from backend.api.schemas.base import BaseSchema
from backend.api.schemas.posts import SubdivisionPost


class User(BaseSchema):
    id: int
    email: str
    first_name: str
    last_name: str
    patronymic: str
    is_admin: bool
    is_teacher: bool
    posts: list[SubdivisionPost]


class DbUser(User):
    password: str


class Token(BaseSchema):
    access_token: str
    token_type: str


class TokenData(BaseSchema):
    email: str | None = None


class PatchUser(BaseSchema):
    email: str | None
    first_name: str | None
    last_name: str | None
    patronymic: str | None
    posts: list[int] | None
