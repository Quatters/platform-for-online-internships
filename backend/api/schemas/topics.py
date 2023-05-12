from backend.api.schemas.base import BaseSchema


class OneTopic(BaseSchema):
    id: int
    name: str

class Topic(BaseSchema):
    id: int
    course_id: int
    name: str
    description: str

class CreateTopic(BaseSchema):
    name: str
    description: str

class PatchTopic(BaseSchema):
    name: str | None
    description: str | None
