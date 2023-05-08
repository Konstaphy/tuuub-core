from uuid import uuid4

from src.db import db
from src.modules.users.model.user_model import User
from src.modules.users.model.request import SignUpRequest
from src.modules.videos.service.s3_service import S3Service


class UserService:
    def __init__(self, s3_service: S3Service):
        self.db = db
        # taking s3 for avatar uploading
        self.s3service = s3_service

    def login(self, username: str, password: str) -> str:
        user = User.get(User.username == username)
        if user and user.password == password:
            return user.id
        # register service logic
        raise ValueError("Invalid username or password")

    def sign_up(self, body: SignUpRequest) -> str:
        user = User(id=str(uuid4()), username=body.username, email=body.email, password=body.password, age=body.age)
        user.save(force_insert=True)

        return user.id

