from flask import Blueprint, jsonify, request
from src.database.s3_client import s3client

video_view = Blueprint('video', __name__)


@video_view.route('/upload')
def upload():
    # Get the uploaded file data from the request object
    file = request.files['file']

    # Upload the file to S3
    s3client.upload_fileobj(file, 'tuuub', 'videos')

    return 'File uploaded successfully!'


@video_view.route('/get')
def load_all():
    # register view logic
    return jsonify({'message': 'videos'})
