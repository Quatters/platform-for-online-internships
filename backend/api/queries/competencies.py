from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session
from backend.api.dependencies import ListPageParams
from backend.api.queries.helpers import get_instances_or_400, with_search
from backend.api.schemas import competencies as schemas
from backend.models.competencies import Competence
from backend.models.courses import Course


def get_competencies(db: Session, params: ListPageParams):
    query = db.query(Competence)
    query = with_search(Competence.name, query=db.query(Competence), search=params.search)
    return paginate(query, params)


def get_competence(db: Session, competence_id: int) -> Competence | None:
    return db.query(Competence).get(competence_id)


def create_competence(db: Session, competence: schemas.CreateCompetence) -> Competence:
    created_competence = Competence(**competence.dict(exclude={'courses'}))
    created_competence.courses = get_instances_or_400(db, Course, competence.courses)
    db.add(created_competence)
    db.commit()
    db.refresh(created_competence)
    return created_competence


def delete_competence(db: Session, competence: Competence):
    db.delete(competence)
    db.commit()


def patch_competence(db: Session, competence: Competence, data: schemas.PatchCompetence) -> Competence:
    db.query(Competence).filter(Competence.id == competence.id).update(data.dict(exclude_unset=True))
    db.commit()
    db.refresh(competence)
    return competence
