from backend.api.schemas.base import BaseSchema
from backend.api.schemas.courses import Course
from backend.api.schemas.posts import Post


class Competence(BaseSchema):
    id: int
    name: str


class OneCompetence(Competence):
    courses: list[Course]
    posts: list[Post]


class CreateCompetence(BaseSchema):
    name: str
    courses: list[int]
    posts: list[int]


class PatchCompetence(BaseSchema):
    name: str | None
    courses: list[int] | None
    posts: list[int] | None
