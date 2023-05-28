from backend.api.schemas.base import BaseSchema


class Course(BaseSchema):
    id: int
    name: str


class FkPost(BaseSchema):
    id: int
    subdivision_id: int
    name: str


class OneCourse(BaseSchema):
    id: int
    name: str
    description: str
    posts: list[FkPost]


class CreateCourse(BaseSchema):
    name: str
    description: str


class PatchCourse(BaseSchema):
    name: str | None
    description: str | None
