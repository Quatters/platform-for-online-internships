from backend.api.schemas.base import BaseSchema
from backend.api.schemas.courses import Course


class SubdivisionPost(BaseSchema):
    id: int
    name: str


class Post(SubdivisionPost):
    subdivision_id: int


class FkCompetence(BaseSchema):
    id: int
    name: str


class OneSubdivisionPost(SubdivisionPost):
    description: str
    courses: list[Course]
    competencies: list[FkCompetence]


class CreateSubdivisionPost(BaseSchema):
    name: str
    description: str
    courses: list[int]
    competencies: list[int]


class PatchSubdivisionPost(BaseSchema):
    name: str | None
    description: str | None
    courses: list[int] | None
    competencies: list[int] | None
