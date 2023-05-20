from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session
from backend.api.queries.helpers import with_search
from backend.models import Subdivision
from backend.api.schemas import subdivisions as schemas
from backend.api.dependencies import ListPageParams


def get_subdivisions(db: Session, params: ListPageParams):
    query = with_search(Subdivision.name, query=db.query(Subdivision), search=params.search)
    return paginate(query, params)


def get_subdivision(db: Session, id: int):
    return db.query(Subdivision).get(id)


def create_subdivision(db: Session, subdivision: schemas.CreateSubdivision):
    subdivision = Subdivision(**subdivision.dict())
    db.add(subdivision)
    db.commit()
    db.refresh(subdivision)
    return subdivision


def delete_subdivision(db: Session, subdivision: Subdivision):
    db.delete(subdivision)
    db.commit()


def update_subdivision(db: Session, subdivision: Subdivision, data: schemas.PatchSubdivision):
    db.query(Subdivision).filter(Subdivision.id == subdivision.id).update(
        data.dict(exclude_unset=True)
    )
    db.commit()
    db.refresh(subdivision)
    return subdivision
