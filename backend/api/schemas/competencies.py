from backend.api.schemas.base import BaseSchema


class Competence(BaseSchema):
    id: int
    name: str


class CreateCompetence(BaseSchema):
    name: str


class PatchCompetence(BaseSchema):
    name: str | None
