from datetime import datetime
from backend.api.schemas.base import BaseSchema
from backend.api.schemas.courses import Course
from backend.constants import TaskType, TestAttemptStatus


class FkTopic(BaseSchema):
    id: int
    course_id: int
    name: str



class PossibleAnswer(BaseSchema):
    id: int
    value: str


class Task(BaseSchema):
    id: int
    name: str
    description: str
    task_type: TaskType
    possible_answers: list[PossibleAnswer] | None


class GoingTest(BaseSchema):
    id: int
    started_at: datetime
    time_to_pass: int
    tasks: list[Task]
    topic: FkTopic


class UserAnswer(BaseSchema):
    task_id: int
    answer: int | list[int] | str


class FinishTestResponse(BaseSchema):
    detail: str = 'Test submitted.'

class ListTest(BaseSchema):
    id: int
    course: Course
    topic: FkTopic
    status: TestAttemptStatus


class OneTest(ListTest):
    score: int
    max_score: int
    started_at: datetime
    finished_at: datetime | None
