from pydantic import BaseModel


class UserTokenData(BaseModel):
    id: str
    username: str
