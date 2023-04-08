from src.db import db
from src.modules.users.model.user_model import User
from src.modules.videos.controller.s3_controller import S3Controller


class UserController:
    def __init__(self, s3controller: S3Controller):
        self.db = db
        # taking s3 for avatar uploading
        self.s3controller = s3controller

    def login(self, username: str, password: str):
        user = User.get(User.username == username)
        if user and user.password == password:
            return user.id
        # register view logic
        raise ValueError("Invalid username or password")
