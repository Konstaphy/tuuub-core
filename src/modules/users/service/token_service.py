import os
from datetime import datetime, timedelta

import jwt

from src.modules.users.model.token_data import UserTokenData
from src.shared.exceptions.authorization_exception import AuthorizationError


class TokenService:
    def generate_new(self, payload: UserTokenData):
        try:
            return jwt.encode(
                {
                    "id": payload.id,
                    "username": payload.username,
                    "exp": datetime.utcnow() + timedelta(days=3),
                },
                os.environ.get("JWT_SECRET"),
                algorithm="HS256")
        except Exception:
            raise AuthorizationError("Unauthorized")

    def validate(self, token: str) -> UserTokenData:
        try:
            data = jwt.decode(token, os.environ.get("JWT_SECRET"), algorithms="HS256")
        except Exception:
            raise AuthorizationError("Unauthorized")

        if data.get("id") is None:
            raise AuthorizationError("Unauthorized")

        return data
