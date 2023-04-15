from flask import Blueprint, jsonify
from flask_cors import cross_origin
from flask_pydantic import validate

from src.modules.users.controller.token_controller import TokenController
from src.modules.users.controller.user_controller import UserController
from src.modules.users.model.token_data import UserTokenData
from src.modules.users.view.request import SignUpRequest, SignInRequest
from src.modules.videos.controller.s3_controller import S3Controller

users_view = Blueprint('users', __name__, url_prefix="/users")

###
# todo: make try excepts
###


@users_view.route('/sign-in', methods=["POST"])
@cross_origin(supports_credentials=True)
@validate()
def login(body: SignInRequest):
    if body.username is None or body.password is None:
        return "Unauthorized", 403

    s3c = S3Controller()
    try:
        user_id = UserController(s3c).login(body.username, body.password)
    except Exception:
        return "Unauthorized", 403

    if user_id is None:
        return "Unauthorized", 403

    token_controller = TokenController()
    token = token_controller.generate_new(UserTokenData(user_id=str(user_id), username=body.username))

    return jsonify({'token': token, 'user_id': str(user_id)})


@users_view.route('/sign-up', methods=["POST"])
@cross_origin(supports_credentials=True)
@validate()
def register(body: SignUpRequest):
    # initializing dependencies
    s3c = S3Controller()
    # making new user
    user_id = UserController(s3c).sign_up(body)

    token_controller = TokenController()
    token = token_controller.generate_new(UserTokenData(user_id=str(user_id), username=body.username))
    # [username, password] = request.authorization
    # register view logic
    return jsonify({'token': token, 'user_id': str(user_id)})
