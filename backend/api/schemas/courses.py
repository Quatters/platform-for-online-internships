from pydantic import Field
from backend.api.schemas.base import BaseSchema


class Course(BaseSchema):
    id: int
    name: str


class FkPost(BaseSchema):
    id: int
    subdivision_id: int
    name: str


class FkCompetence(BaseSchema):
    id: int
    name: str


class OneCourse(Course):
    description: str
    pass_percent: float
    posts: list[FkPost]
    competencies: list[FkCompetence]


class CreateCourse(BaseSchema):
    name: str
    description: str
    pass_percent: float = Field(ge=1, le=100, default=86)
    posts: list[int]
    competencies: list[int]


class PatchCourse(BaseSchema):
    name: str | None
    description: str | None
    pass_percent: float | None = Field(ge=1, le=100, default=None)
    posts: list[int] | None
    competencies: list[int] | None
