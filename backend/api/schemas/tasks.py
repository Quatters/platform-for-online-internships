from backend.api.schemas.base import BaseSchema
from backend.models.task_types import TaskType


class Task(BaseSchema):
    id: int
    name: str
    prev_task_id: int | None
    task_type: TaskType

class OneTask(BaseSchema):
    id: int
    topic_id: int
    name: str
    description: str
    prev_task_id: int | None
    task_type: TaskType

class CreateTask(BaseSchema):
    name: str
    description: str
    prev_task_id: int | None
    task_type: TaskType

class PatchTask(BaseSchema):
    name: str | None
    description: str | None
    prev_topic_id: int | None
    task_type: TaskType | None
