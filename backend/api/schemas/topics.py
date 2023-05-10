from backend.api.schemas.base import BaseSchema


class OneTopic(BaseSchema):
    id: int
    name: str

class Topic(BaseSchema):
    id: int
    name: str
    description: str
