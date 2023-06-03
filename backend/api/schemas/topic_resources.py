from backend.api.schemas.base import BaseSchema
from backend.constants import TopicResourceType


class ListTopicResource(BaseSchema):
    id: int
    type: TopicResourceType
    name: str
    value: str


class FkTopicResource(BaseSchema):
    id: int
    name: str


class OneTopicResource(ListTopicResource):
    prev_resource: FkTopicResource | None
    next_resource: FkTopicResource | None


class PatchTopicResource(BaseSchema):
    type: TopicResourceType | None
    name: str | None
    value: str | None


class CreateTopicResource(BaseSchema):
    type: TopicResourceType
    name: str
    value: str
