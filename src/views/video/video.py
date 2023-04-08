from flask import Blueprint, jsonify
video_view = Blueprint('users', __name__)


@video_view.route('/upload')
def upload():
    # login view logic
    return jsonify({'message': 'uploaded'})


@video_view.route('/get')
def load_all():
    # register view logic
    return jsonify({'message': 'videos'})
