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
    name: str | None
    value: str | None
    prev_resource_id: int | None


class CreateTopicResource(BaseSchema):
    type: TopicResourceType
    name: str
    value: str
    prev_resource_id: int | None
