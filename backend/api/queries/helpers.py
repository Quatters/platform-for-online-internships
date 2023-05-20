from typing import Callable
from sqlalchemy import func, or_


def with_search(*fields, query, search: str):
    if search:
        filters = [
            func.lower(field).like(f'%{search.lower()}%')
            for field in fields
        ]
        query = query.filter(or_(*filters))
    return query
