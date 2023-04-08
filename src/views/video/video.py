from flask import Blueprint, jsonify, request
from flask_cors import cross_origin

from src.database.s3_client import s3client

video_view = Blueprint('videos', __name__, url_prefix="/videos")


@video_view.route('/upload', methods=["POST"])
@cross_origin(supports_credentials=True)
def upload():
    print(request.files)
    # Get the uploaded file data from the request object
    file = request.files['video']

    # Upload the file to S3
    s3client.upload_fileobj(file, 'tuuub', 'videos/' + file.filename)

    return 'File uploaded successfully!'


@video_view.route('/get')
def load_all():
    # register view logic
    return jsonify({'message': 'videos'})
