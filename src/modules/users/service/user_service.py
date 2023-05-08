from uuid import uuid4

from peewee import DoesNotExist
from psycopg2.errors import UniqueViolation

from src.db import db
from src.modules.users.model.user_model import User
from src.modules.users.model.request import SignUpRequest
from src.modules.videos.service.s3_service import S3Service
from src.shared.exceptions.authorization_exception import AuthorizationError
from src.shared.utils.auth.encrypt_password import encrypt_password


class UserService:
    def __init__(self, s3_service: S3Service):
        self.db = db
        # taking s3 for avatar uploading
        self.s3service = s3_service

    def login(self, username: str, password: str) -> str:
        try:
            user = User.get(User.username == username)
        except DoesNotExist:
            raise AuthorizationError("Users does not exist")

        if user and encrypt_password(password) == user.password:
            return user.id

        # If user not found throw an error
        raise AuthorizationError("Invalid username or password")

    def sign_up(self, body: SignUpRequest) -> str:
        try:
            user = User(id=str(uuid4()),
                        username=body.username,
                        email=body.email,
                        password=encrypt_password(body.password),
                        age=body.age)
        except UniqueViolation:
            raise AuthorizationError("User already exists")

        user.save(force_insert=True)
        return user.id

    def check_for_existence(self, username: str, email: str) -> False:
        # If user with username or email already exists
        try:
            User.get((User.username == username) | (User.email == email))
        except DoesNotExist:
            return False

        # If user found throw an error
        raise AuthorizationError("User already exists")

