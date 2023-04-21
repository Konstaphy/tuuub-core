from flask import Blueprint, jsonify, request, Response
from flask_cors import cross_origin

from src.modules.users.model.token_data import UserTokenData
from src.modules.videos.service.s3_service import S3Controller, S3Exception
from src.utils.tokenized_decorator import tokenized

video_view = Blueprint('videos', __name__, url_prefix="/videos")

###
#
# ! IMPORTANT !
# Next two routes are necessary to work with s3
# be careful with changing sth in them
#
# ###


@video_view.route('/upload', methods=["POST"])
@cross_origin(supports_credentials=True)
@tokenized
def upload():
    # Get the uploaded file data from the request object
    file = request.files['video']
    # Upload the file to S3
    try:
        S3Controller().upload_video(file)
    except S3Exception:
        return 'Failed to upload video', 500

    return 'File uploaded successfully!', 200


# proxy for videos and images
# unauthorized!!!
@video_view.route('/s3')
@cross_origin(supports_credentials=True)
def s3proxy():
    # get the key from the request
    key = request.args.get('key')
    # get the file from s3
    try:
        file = S3Controller().get_file(key)
    except S3Exception:
        return 'Failed to get file', 500

    # return the file
    return Response(file, mimetype='video/mp4')


# recommendation system would be implemented here
@video_view.route('/get')
@tokenized
def load_all(data: UserTokenData):
    # register service logic
    return jsonify({'message': 'videos'})
