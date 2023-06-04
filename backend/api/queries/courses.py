from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session
from backend.models import Course
from backend.api.schemas import courses as schemas
from backend.api.dependencies import ListPageParams
from backend.api.queries.helpers import get_instances_or_400, with_search
from backend.models.competencies import Competence


def get_courses(db: Session, params: ListPageParams):
    query = with_search(Course.name, query=db.query(Course), search=params.search)
    query = query.order_by(Course.name)
    return paginate(query, params)


def get_course(db: Session, id: int) -> Course | None:
    return db.query(Course).get(id)


def get_course_by_name(db: Session, name: str) -> Course | None:
    return db.query(Course).filter(Course.name == name).one_or_none()


def create_course(db: Session, course: schemas.CreateCourse) -> Course:
    created_course = Course(**course.dict())
    created_course.competencies = get_instances_or_400(db, Competence, course.competencies)
    db.add(created_course)
    db.commit()
    db.refresh(created_course)
    return created_course


def delete_course(db: Session, course: Course):
    db.delete(course)
    db.commit()


def patch_course(db: Session, course: Course, data: schemas.PatchCourse) -> Course:
    dict_ = data.dict(exclude_unset=True)
    if 'competencies' in dict_:
        course.competencies = get_instances_or_400(db, Competence, dict_.pop('competencies'))
    for key, value in dict_.items():
        setattr(course, key, value)
    db.commit()
    db.refresh(course)
    return course
