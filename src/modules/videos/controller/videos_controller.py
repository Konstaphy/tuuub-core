import uuid

import requests
from flask import Blueprint, jsonify, request, Response
from flask_cors import cross_origin
from flask_pydantic import validate
from pydantic import BaseModel

from src.modules.reactions.model.reaction_model import Reaction
from src.modules.videos.model.video_model import Video
from src.modules.videos.service.s3_service import S3Service, S3Exception
from src.shared.utils.auth.tokenized_decorator import tokenized

video_controller = Blueprint('videos', __name__, url_prefix="/videos")


def get_user_info():
    try:
        token = request.headers.get("Authorization").split(" ")[1]
    except Exception as e:
        return "No token", 403

    data = requests.get("https://login.yandex.ru/info?format=json", headers={"Authorization": f"OAuth {token}"})
    return data.json()

###
#
# ! IMPORTANT !
# Next two routes are necessary to work with s3
# be careful with changing sth in them
#
# ###



@video_controller.route('/upload', methods=["POST"])
@cross_origin(supports_credentials=True)
def upload():
    user_data = get_user_info()
    # Get the uploaded file data from the request object
    try:
        file = request.files['video']
    except Exception as e:
        return "File not found by key 'video'", 500
    # Upload the file to S3
    try:
        filename = S3Service().upload_video(file)
    except S3Exception as e:
        print(e)
        return 'Failed to upload video', 500

    video = Video.create(id=uuid.uuid4(),
                         file_path=filename,
                         # все остальное апдейтится в другом роуте
                         title="",
                         description="",
                         photo_path="",
                         user_id=user_data.get("id"))
    video.save()

    return video.id, 200


class UpdateResponse(BaseModel):
    video_id: str
    video_name: str
    video_description: str | None = None


@video_controller.route('/update', methods=["POST"])
@cross_origin(supports_credentials=True)
@validate()
def update(body: UpdateResponse):
    video = Video.update(title=body.video_name, description=body.video_description or "").where(Video.id == body.video_id)
    video.execute()
    return body.video_id


# proxy for videos and images
# unauthorized!!!
@video_controller.route('/s3')
@cross_origin(supports_credentials=True)
def s3proxy():
    # get the key from the request
    key = request.args.get('key')
    # get the file from s3
    try:
        file = S3Service().get_file(key)
    except S3Exception:
        return 'Failed to get file', 500

    # return the file
    return Response(file, mimetype='video/mp4')


class GetVideoReactions(BaseModel):
    video_id: str


@video_controller.route('/get_reactions', methods=["POST"])
@cross_origin(supports_credentials=True)
@tokenized()
def get_video_reactions(body: GetVideoReactions):
    reactions: list[Reaction] = Video.get(id=body.video_id).reactions
    return jsonify({'reactions': [str(r.user_id) for r in reactions]})


# recommendation system would be implemented here
@video_controller.route('/get', methods=["GET"])
@cross_origin(supports_credentials=True)
def load_all():
    # register service logic
    videos = [v for v in Video.select().dicts()]
    return jsonify({'videos': videos})



@video_controller.route('/get_by_id')
@cross_origin(supports_credentials=True)
def load_all_by_person():
    # register service logic
    user_data = get_user_info()
    videos = [v for v in Video.select().where(Video.user_id == user_data.get("id")).dicts()]
    return videos


@video_controller.route('/get_video/<video_id>', methods=["GET"])
@cross_origin(supports_credentials=True)
def get_video(video_id: str):
    results = Video.select().where(Video.id == video_id).limit(1).dicts()
    video = results[0] if len(results) > 0 else None
    print(video)
    return video
