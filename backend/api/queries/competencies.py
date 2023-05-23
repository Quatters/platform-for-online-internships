from typing import List
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import func
from sqlalchemy.orm import Session
from backend.api.dependencies import ListPageParams
from backend.api.schemas import competencies as schemas
from backend.models.competencies import Competence


def get_competencies(db: Session, params: ListPageParams) -> List[Competence]:
    query = db.query(Competence)
    if s := params.search:
        query = query.filter(func.lower(Competence.name).like(f'%{s.lower()}%'))
    return paginate(query, params)


def get_competence(db: Session, competence_id: int) -> Competence | None:
    return db.query(Competence).get(competence_id)


def create_competence(db: Session, competence: schemas.CreateCompetence) -> Competence:
    competence = Competence(**competence.dict())
    db.add(competence)
    db.commit()
    db.refresh(competence)
    return competence


def delete_competence(db: Session, competence: Competence):
    db.delete(competence)
    db.commit()


def patch_competence(db: Session, competence: Competence, data: schemas.PatchCompetence) -> Competence:
    db.query(Competence).filter(Competence.id == competence.id).update(data.dict(exclude_unset=True))
    db.commit()
    db.refresh(competence)
    return competence

