from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.api.auth import admin_only
from backend.api.current_dependencies import current_course, get_current_competence, get_current_course_competence
from backend.api.dependencies import ListPageParams
from backend.api.errors.errors import not_found
from backend.database import get_db
from backend.api.queries import course_competencies as queries
from backend.api.queries import competencies as queries_competencies
from backend.api.schemas import course_competencies as schemas
from backend.api.schemas import courses as schemas_courses
from backend.models.competencies import Competence
from backend.models.course_competencies import CourseCompetence
from backend.models.courses import Course
from backend.settings import LimitOffsetPage


router = APIRouter(prefix='')


@router.get('/courses/{course_id}/competencies/', response_model=LimitOffsetPage[schemas.CourseCompetence])
def get_course_competencies(course: Course = Depends(current_course),
                            params: ListPageParams = Depends(),
                            db: Session = Depends(get_db)):
    return queries.get_course_competencies(db, params, course.id)


@router.get('/competencies/{competence_id}/courses/', response_model=LimitOffsetPage[schemas_courses.Course])
def get_related_courses(competence: Competence = Depends(get_current_competence),
                        params: ListPageParams = Depends(),
                        db: Session = Depends(get_db)):
    return queries.get_courses(db, params, competence.id)


@router.post('/courses/{course_id}/competencies/',
             response_model=schemas.CourseCompetence,
             dependencies=[Depends(admin_only)])
def create_competence(course_competence: schemas.CreateCourseCompetence,
                      course: Course = Depends(current_course),
                      db: Session = Depends(get_db)):
    competence = queries_competencies.get_competence(db, course_competence.competence_id)
    if competence is None:
        raise not_found()
    created = queries.create_course_competence(db, course_competence, course.id)
    created.course_name = created.course.name
    created.competence_name = created.competence.name
    return created


@router.delete('/courses/{course_id}/competencies/{course_competence_id}',
               status_code=204,
               dependencies=[Depends(admin_only)])
def delete_compentence(course_competence: CourseCompetence = Depends(get_current_course_competence),
                       db: Session = Depends(get_db)):
    queries.delete_course_competence(db, course_competence)
    return {}
