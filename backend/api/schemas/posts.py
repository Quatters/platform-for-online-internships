from backend.api.schemas.base import BaseSchema


class Post(BaseSchema):
    id: int
    name: str


class OnePost(Post):
    description: str


class CreatePost(BaseSchema):
    name: str
    description: str


class PatchPost(BaseSchema):
    name: str | None
    description: str | None
