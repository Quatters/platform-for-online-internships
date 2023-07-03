from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.api.auth import admin_only, intern_only
from backend.api.current_dependencies import get_current_course
from backend.database import get_db
from backend.api.queries import courses as queries
from backend.api.schemas import courses as schemas
from backend.models import Course, User
from backend.settings import LimitOffsetPage
from backend.api.dependencies import ListPageParams, RecommendedCoursesListPageParams


router = APIRouter(prefix='/courses')


@router.get('/', response_model=LimitOffsetPage[schemas.Course])
def get_courses(params: ListPageParams = Depends(), db: Session = Depends(get_db)):
    return queries.get_courses(db, params)


@router.get('/recommended', response_model=LimitOffsetPage[schemas.Course])
def get_recommended_courses(
    user: User = Depends(intern_only),
    params: RecommendedCoursesListPageParams = Depends(),
    db: Session = Depends(get_db),
):
    return queries.get_recommended_courses(db, user, params)


@router.get('/{course_id}', response_model=schemas.OneCourse)
def get_course(course: Course = Depends(get_current_course)):
    return course


@router.post('/',
             response_model=schemas.OneCourse,
             dependencies=[Depends(admin_only)])
def create_course(course: schemas.CreateCourse,
                  db: Session = Depends(get_db)):
    created_course = queries.create_course(db, course)
    return created_course


@router.delete('/{course_id}',
               status_code=204,
               dependencies=[Depends(admin_only)])
def delete_course(course: Course = Depends(get_current_course),
                  db: Session = Depends(get_db)):
    queries.delete_course(db, course)
    return {}


@router.patch('/{course_id}',
              response_model=schemas.OneCourse,
              dependencies=[Depends(admin_only)])
def patch_course(course: schemas.PatchCourse,
                 course_to_patch: Course = Depends(get_current_course),
                 db: Session = Depends(get_db)):
    queries.patch_course(db, course_to_patch, course)
    return course_to_patch
