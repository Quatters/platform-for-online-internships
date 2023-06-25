from typing import Literal
from backend.settings import LimitOffsetParams
from backend.constants import UserAnswerStatus, TestAttemptStatus


class ListPageParams(LimitOffsetParams):
    search: str | None


class UserListPageParams(ListPageParams):
    role: Literal['admin', 'teacher', 'intern'] | None


class ReviewListPageParams(ListPageParams):
    status: UserAnswerStatus | None


class TestAttemptListPageParams(ListPageParams):
    status: TestAttemptStatus | None


class PostsListPageParams(ListPageParams):
    subdivision_id: int | None
