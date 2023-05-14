from backend.api.schemas.base import BaseSchema


class OneTopic(BaseSchema):
    id: int
    name: str
    prev_topic_id: int | None

class Topic(BaseSchema):
    id: int
    course_id: int
    name: str
    description: str
    prev_topic_id: int | None

class CreateTopic(BaseSchema):
    name: str
    description: str
    prev_topic_id: int | None

class PatchTopic(BaseSchema):
    name: str | None
    description: str | None
    prev_topic_id: int | None
