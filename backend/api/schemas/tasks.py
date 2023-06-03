from backend.api.schemas.base import BaseSchema
from backend.constants import TaskType


class Task(BaseSchema):
    id: int
    name: str
    task_type: TaskType


class FkTask(BaseSchema):
    id: int
    name: str


class OneTask(BaseSchema):
    id: int
    name: str
    description: str
    prev_task: FkTask | None
    next_task: FkTask | None
    task_type: TaskType


class CreateTask(BaseSchema):
    name: str
    description: str
    prev_task_id: int | None
    task_type: TaskType


class PatchTask(BaseSchema):
    name: str | None
    description: str | None
    prev_task_id: int | None
