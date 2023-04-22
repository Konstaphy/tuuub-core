import uuid

from flask import Blueprint, jsonify, request, Response
from flask_cors import cross_origin
from flask_pydantic import validate
from pydantic import BaseModel

from src.modules.reactions.model.reaction_model import Reaction
from src.modules.users.model.token_data import UserTokenData
from src.modules.videos.model.video_model import Video
from src.modules.videos.service.s3_service import S3Service, S3Exception
from src.shared.utils.auth.tokenized_decorator import tokenized

video_controller = Blueprint('videos', __name__, url_prefix="/videos")


###
#
# ! IMPORTANT !
# Next two routes are necessary to work with s3
# be careful with changing sth in them
#
# ###


@video_controller.route('/upload', methods=["POST"])
@cross_origin(supports_credentials=True)
@tokenized()
def upload(data: UserTokenData):
    # Get the uploaded file data from the request object
    try:
        file = request.files['video']
    except Exception as e:
        return "File not found by key 'video'", 500
    # Upload the file to S3
    try:
        S3Service().upload_video(file)
    except S3Exception:
        return 'Failed to upload video', 500

    Video.create(id=uuid.uuid4(),
                 file_path=file.filename,
                 title="123",
                 description="",
                 user_id=data.id).save()

    return 'File uploaded successfully!', 200


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
@tokenized()
@validate()
def get_video_reactions(token_data: UserTokenData, body: GetVideoReactions):
    reactions: list[Reaction] = Video.get(id=body.video_id).reactions
    return jsonify({'reactions': [str(r.user_id) for r in reactions]})


# recommendation system would be implemented here
@video_controller.route('/get')
@tokenized()
def load_all(data: UserTokenData):
    # register service logic
    return jsonify({'message': 'videos'})
