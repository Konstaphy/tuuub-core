import os

import requests
from flask import Blueprint
from flask_cors import cross_origin

from src.modules.users.model.user_model import User

users_controller = Blueprint('users', __name__, url_prefix="/users")


@users_controller.route("/token/<code>", methods=["GET"])
@cross_origin(supports_credentials=True)
def get_token_by_code(code: str):
    data = requests.post("https://oauth.yandex.ru/token", f"grant_type=authorization_code"
                                                          f"&code={code}"
                                                          f"&client_id={os.getenv('YA_ID')}"
                                                          f"&client_secret={os.getenv('YA_SECRET')}")
    return data.json()


@users_controller.route("/user/<token>", methods=["GET"])
@cross_origin(supports_credentials=True)
def get_user_by_token(token: str):
    data = requests.get("https://login.yandex.ru/info?format=json", headers={"Authorization": f"OAuth {token}"})
    user_data = data.json()
    user_id = user_data.get("id")
    if not User.select().where(User.id == user_id).exists():
        User.create(id=user_id)
    return data.json()
