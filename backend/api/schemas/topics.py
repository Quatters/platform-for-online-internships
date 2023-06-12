from pydantic import Field
from backend.api.schemas.base import BaseSchema


class Topic(BaseSchema):
    id: int
    name: str


class OneTopic(BaseSchema):
    id: int
    name: str
    description: str
    attempts_amount: int
    prev_topic: Topic | None
    next_topic: Topic | None


class CreateTopic(BaseSchema):
    name: str
    description: str
    attempts_amount: int = Field(default=3, ge=1)
    prev_topic_id: int | None


class PatchTopic(BaseSchema):
    name: str | None
    description: str | None
    attempts_amount: int | None = Field(default=None, ge=1)
    prev_topic_id: int | None
    next_topic_id: int | None
