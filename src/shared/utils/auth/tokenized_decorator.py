import os
from functools import wraps
from typing import Callable

import jwt
from flask import request
from flask_pydantic import validate

from src.modules.users.model.token_data import UserTokenData


def get_data_by_token() -> UserTokenData:
    try:
        token = request.headers["authorization"].split(" ")[1]
    except KeyError:
        raise ValueError("Unauthorized: Failed to parse token")

    if token is None:
        raise ValueError("Unauthorized: No token")

    try:
        data = jwt.decode(token, os.environ.get("JWT_SECRET"), algorithms="HS256")
    except Exception as e:
        raise ValueError("Unauthorized: Failed to decode token")

    if data.get("id") is None:
        raise ValueError("Unauthorized: No id found in token declaration")

    return UserTokenData(id=data.get("id"), username=data.get("username"))


# decorator for checking token validity
def tokenized():
    def decorate(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            # get user data by token
            try:
                data = get_data_by_token()
            except ValueError as e:
                return e.__str__(), 403
            return func(token_data=data, *args, **kwargs)

        return wrapper

    return decorate
