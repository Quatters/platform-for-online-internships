from datetime import datetime
from backend.api.schemas.base import BaseSchema
from backend.constants import TaskType


class PossibleAnswer(BaseSchema):
    id: int
    value: str


class Task(BaseSchema):
    id: int
    name: str
    description: str
    task_type: TaskType
    possible_answers: list[PossibleAnswer] | None


class NewTest(BaseSchema):
    id: int
    started_at: datetime
    time_to_pass: int
    tasks: list[Task]
