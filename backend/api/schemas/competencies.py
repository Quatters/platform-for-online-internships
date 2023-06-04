from backend.api.schemas.base import BaseSchema
from backend.api.schemas.courses import Course


class Competence(BaseSchema):
    id: int
    name: str


class OneCompetence(Competence):
    courses: list[Course]


class CreateCompetence(BaseSchema):
    name: str
    courses: list[int]


class PatchCompetence(BaseSchema):
    name: str | None
    courses: list[int] | None
