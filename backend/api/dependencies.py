from typing import Literal
from backend.settings import LimitOffsetParams


class ListPageParams(LimitOffsetParams):
    search: str | None


class UserListPageParams(ListPageParams):
    role: Literal['admin', 'teacher', 'intern'] | None
