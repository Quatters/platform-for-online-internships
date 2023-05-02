from backend.api.schemas.base import BaseSchema


class Course(BaseSchema):
    id: int
    name: str


class OneCourse(BaseSchema):
    id: int
    name: str
    description: str


class CreateCourse(BaseSchema):
    name: str
    description: str


class PatchCourse(BaseSchema):
    name: str | None
    description: str | None
