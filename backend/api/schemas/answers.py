from backend.api.schemas.base import BaseSchema


class Answer(BaseSchema):
    id: int
    value: str
    task_id: int


class AnswerAdmin(BaseSchema):
    id: int
    value: str
    task_id: int
    is_correct: bool


class CreateAnswer(BaseSchema):
    value: str
    is_correct: bool


class PatchAnswer(BaseSchema):
    value: str | None
    is_correct: bool | None
