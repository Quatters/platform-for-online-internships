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
    posts: list[FkPost]
    competencies: list[FkCompetence]


class CreateCourse(BaseSchema):
    name: str
    description: str
    posts: list[int]
    competencies: list[int]


class PatchCourse(BaseSchema):
    name: str | None
    description: str | None
    posts: list[int] | None
    competencies: list[int] | None
