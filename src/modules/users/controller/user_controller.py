from uuid import uuid4

from src.db import db
from src.modules.users.model.user_model import User
from src.modules.users.view.request import SignUpRequest
from src.modules.videos.controller.s3_controller import S3Controller


class UserController:
    def __init__(self, s3_controller: S3Controller):
        self.db = db
        # taking s3 for avatar uploading
        self.s3controller = s3_controller

    def login(self, username: str, password: str) -> str:
        user = User.get(User.username == username)
        if user and user.password == password:
            return user.id
        # register view logic
        raise ValueError("Invalid username or password")

    def sign_up(self, body: SignUpRequest) -> str:
        user = User(id=str(uuid4()), username=body.username, email=body.email, password=body.password, age=body.age)
        user.save(force_insert=True)

        return user.id

