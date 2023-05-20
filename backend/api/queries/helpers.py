from typing import TypeVar
from sqlalchemy import func, or_, Column
from sqlalchemy.orm import Query


T = TypeVar('T')


def with_search(*fields: Column[str], query: Query[T], search: str | None) -> Query[T]:
    if search:
        filters = [
            func.lower(field).like(f'%{search.lower()}%')
            for field in fields
        ]
        query = query.filter(or_(*filters))
    return query
