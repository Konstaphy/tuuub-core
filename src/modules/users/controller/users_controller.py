from flask import Blueprint, jsonify
from flask_cors import cross_origin
from flask_pydantic import validate

from src.modules.users.service.token_service import TokenController
from src.modules.users.service.user_service import UserService
from src.modules.users.model.token_data import UserTokenData
from src.modules.users.model.request import SignUpRequest, SignInRequest
from src.modules.videos.service.s3_service import S3Service
from src.shared.exceptions.authorization_exception import AuthorizationError

users_controller = Blueprint('users', __name__, url_prefix="/users")

###
# todo: make try excepts
###


@users_controller.route('/sign-in', methods=["POST"])
@cross_origin(supports_credentials=True)
@validate()
def login(body: SignInRequest):
    if body.username is None or body.password is None:
        return "Unauthorized", 403

    s3c = S3Service()
    try:
        user_id = UserService(s3c).login(body.username, body.password)
    except AuthorizationError as e:
        return e.message, 403

    if user_id is None:
        return "Unauthorized", 403

    token_controller = TokenController()
    try:
        token = token_controller.generate_new(UserTokenData(id=str(user_id), username=body.username))
    except Exception as e:
        return "Failed to generate token", 500

    return jsonify({'token': token, 'user_id': str(user_id)})


@users_controller.route('/sign-up', methods=["POST"])
@cross_origin(supports_credentials=True)
@validate()
def register(body: SignUpRequest):
    # initializing dependencies
    s3c = S3Service()
    # making new user
    user_service = UserService(s3c)

    try:
        user_service.check_for_existence(body.username, body.email)
    except AuthorizationError as e:
        return e.message, 409

    try:
        user_id = user_service.sign_up(body)
    except AuthorizationError as e:
        return e.message, 500

    token_controller = TokenController()
    try:
        token = token_controller.generate_new(UserTokenData(id=str(user_id), username=body.username))
    except Exception as e:
        return e, 500

    # register service logic
    return jsonify({'token': token, 'user_id': str(user_id)})
