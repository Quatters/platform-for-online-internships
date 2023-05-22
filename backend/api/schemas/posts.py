from backend.api.schemas.base import BaseSchema


class SubdivisionPost(BaseSchema):
    id: int
    name: str


class Post(SubdivisionPost):
    subdivision_id: int


class OneSubdivisionPost(SubdivisionPost):
    description: str


class CreateSubdivisionPost(BaseSchema):
    name: str
    description: str


class PatchSubdivisionPost(BaseSchema):
    name: str | None
    description: str | None
