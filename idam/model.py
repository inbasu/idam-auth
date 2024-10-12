from pydantic import BaseModel


class User(BaseModel):
    username: str
    email: str
    roles: list[str]
    stores: list[int]
