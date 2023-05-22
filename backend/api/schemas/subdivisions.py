from backend.api.schemas.base import BaseSchema


class Subdivision(BaseSchema):
    id: int
    name: str


class OneSubdivision(Subdivision):
    description: str


class CreateSubdivision(BaseSchema):
    name: str
    description: str


class PatchSubdivision(BaseSchema):
    name: str | None
    description: str | None
