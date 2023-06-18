from pydantic import Field
from backend.api.schemas.base import BaseSchema
from backend.constants import UserAnswerStatus


class ListReview(BaseSchema):
    id: int
    task_name: str
    status: UserAnswerStatus


class Review(ListReview):
    task_description: str
    review: str | None
    value: str | list[str]
    score: int
    max_score: int


class FinishReview(BaseSchema):
    review: str | None
    score: int = Field(ge=0, le=5)
