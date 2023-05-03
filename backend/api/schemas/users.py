from backend.api.schemas.base import BaseSchema


class User(BaseSchema):
    email: str
    first_name: str
    last_name: str
    patronymic: str
    is_admin: bool
    is_teacher: bool


class UserWithId(User):
    id: int


class DbUser(User):
    password: str


class Token(BaseSchema):
    access_token: str
    token_type: str


class TokenData(BaseSchema):
    email: str | None = None
