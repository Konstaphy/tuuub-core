from functools import wraps

import jwt
from flask import request

from src.modules.users.model.token_data import UserTokenData


def get_data_by_token():
    try:
        token = request.headers["authorization"].split(" ")[1]
    except KeyError:
        raise ValueError("Unauthorized")

    if token is None:
        raise ValueError("Unauthorized")

    try:
        data = jwt.decode(token, "secret", algorithms="HS256")
    except Exception as e:
        raise ValueError("Unauthorized")

    if data.get("id") is None:
        raise ValueError("Unauthorized")

    return data


# decorator for checking token validity
def tokenized(func):
    @wraps(func)
    def wrapper():
        # get user data by token
        try:
            data = get_data_by_token()
        except ValueError:
            return "Unauthorized", 401
        return func(UserTokenData(data.get("id"), data.get("username")))

    return wrapper
