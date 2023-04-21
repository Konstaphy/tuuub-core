import os
import jwt

from src.modules.users.model.token_data import UserTokenData


class TokenController:
    def generate_new(self, payload: UserTokenData):
        return jwt.encode(
            {
                "id": payload.id,
                "username": payload.username
            },
            os.environ.get("JWT_SECRET"),
            algorithm="HS256")

    def validate(self, token: str) -> UserTokenData:
        try:
            data = jwt.decode(token, os.environ.get("JWT_SECRET"), algorithms="HS256")
        except Exception:
            raise ValueError("Unauthorized")

        if data.get("id") is None:
            raise ValueError("Unauthorized")

        return data
