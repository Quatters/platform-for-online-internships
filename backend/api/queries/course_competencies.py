from fastapi_pagination import paginate
from sqlalchemy.orm import Session, joinedload
from backend.api.dependencies import ListPageParams
from backend.api.schemas import course_competencies as schemas
from backend.models.competencies import Competence as CompetenceModel
from backend.models.courses import Course as CourseModel
from backend.models.course_competencies import CourseCompetence


def get_course_competencies(db: Session, params: ListPageParams, course_id: int):
    query = db.query(CourseCompetence) \
              .filter(CourseCompetence.course_id == course_id) \
              .options(
                joinedload(CourseCompetence.course, innerjoin=True).load_only(CourseModel.name),
                joinedload(CourseCompetence.competence, innerjoin=True).load_only(CompetenceModel.name)
              )
    objects = query \
            .limit(params.limit) \
            .offset(params.offset) \
            .all()
    for obj in objects:
        obj.course_name = obj.course.name
        obj.competence_name = obj.competence.name

    return paginate(objects, params, length_function=lambda _: query.count())


def get_course_competence(db: Session, course_competence_id: int):
    return db.query(CourseCompetence).get(course_competence_id)


def create_course_competence(db: Session, course_competence: schemas.CreateCourseCompetence, course_id: int):
    course_competence = CourseCompetence(**course_competence.dict())
    course_competence.course_id = course_id
    db.add(course_competence)
    db.commit()
    db.refresh(course_competence)
    return course_competence


def delete_course_competence(db: Session, competence: CourseCompetence):
    db.delete(competence)
    db.commit()
