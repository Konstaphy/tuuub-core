from flask import Blueprint, jsonify, Request, request

from src.modules.users.controller.user_controller import UserController
from src.modules.videos.controller.s3_controller import S3Controller

users_view = Blueprint('users', __name__, url_prefix="/users")


@users_view.route('/sign-in')
def login():
    [username, password] = Request.authorization
    if username is None or password is None:
        return "Unauthorized", 403

    s3c = S3Controller()
    user_id = UserController(s3c).login(username, password)

    if user_id is None:
        return "Unauthorized", 403

    return jsonify({'id': user_id})


@users_view.route('/sign-up', methods=["POST"])
def register():
    [username, password] = request.authorization
    # register view logic
    return jsonify({'message': 'register'})
