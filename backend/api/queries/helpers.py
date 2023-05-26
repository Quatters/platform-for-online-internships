from typing import TypeVar
from sqlalchemy import func, or_, Column
from sqlalchemy.orm import Query, Session
from backend.api.errors.errors import bad_request
from backend.models.base import BaseModel


T = TypeVar('T')
TModel = TypeVar('TModel', bound=BaseModel)


def with_search(*fields: Column[str], query: Query[T], search: str | None) -> Query[T]:
    if search:
        filters = [
            func.lower(field).like(f'%{search.lower()}%')
            for field in fields
        ]
        query = query.filter(or_(*filters))
    return query


def get_instances_or_400(db: Session, model: TModel, ids: list[int]) -> list[TModel]:
    instances = []
    if ids:
        instances = db.query(model).filter(model.id.in_(ids)).all()
    if len(ids) != len(instances):
        raise bad_request('Some of the instances not exist.')
    return instances
