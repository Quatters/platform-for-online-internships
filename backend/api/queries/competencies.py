from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session
from backend.api.dependencies import ListPageParams
from backend.api.queries.helpers import get_instances_or_400, with_search
from backend.api.schemas import competencies as schemas
from backend.models.competencies import Competence
from backend.models.courses import Course
from backend.models.posts import Post


def get_competencies(db: Session, params: ListPageParams):
    query = db.query(Competence)
    query = with_search(Competence.name, query=query, search=params.search)
    return paginate(query, params)


def get_competence(db: Session, competence_id: int) -> Competence | None:
    return db.query(Competence).get(competence_id)


def create_competence(db: Session, competence: schemas.CreateCompetence) -> Competence:
    created_competence = Competence(**competence.dict(exclude={'courses', 'posts'}))
    created_competence.courses = get_instances_or_400(db, Course, competence.courses)
    created_competence.posts = get_instances_or_400(db, Post, competence.posts)
    db.add(created_competence)
    db.commit()
    db.refresh(created_competence)
    return created_competence


def delete_competence(db: Session, competence: Competence):
    db.delete(competence)
    db.commit()


def patch_competence(db: Session, competence: Competence, data: schemas.PatchCompetence) -> Competence:
    dict_ = data.dict(exclude_unset=True)
    if 'courses' in dict_:
        competence.courses = get_instances_or_400(db, Course, dict_.pop('courses'))
    if 'posts' in dict_:
        competence.posts = get_instances_or_400(db, Post, dict_.pop('posts'))
    for key, value in dict_.items():
        setattr(competence, key, value)
    db.commit()
    db.refresh(competence)
    return competence
