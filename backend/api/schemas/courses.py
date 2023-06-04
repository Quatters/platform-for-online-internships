from backend.api.schemas.base import BaseSchema
from backend.api.schemas.competencies import Competence


class Course(BaseSchema):
    id: int
    name: str


class OneCourse(Course):
    description: str
    competencies: list[Competence]


class CreateCourse(BaseSchema):
    name: str
    description: str
    competencies: list[int]


class PatchCourse(BaseSchema):
    name: str | None
    description: str | None
    competencies: list[int] | None
