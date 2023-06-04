from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.api.auth import admin_only
from backend.api.errors.errors import not_found
from backend.database import get_db
from backend.api.queries import courses as queries
from backend.api.schemas import courses as schemas
from backend.settings import LimitOffsetPage
from backend.api.dependencies import ListPageParams


router = APIRouter(prefix='/courses')


@router.get('/', response_model=LimitOffsetPage[schemas.Course])
def get_courses(params: ListPageParams = Depends(), db: Session = Depends(get_db)):
    return queries.get_courses(db, params)


@router.get('/{course_id}', response_model=schemas.OneCourse)
def get_course(course_id: int, db: Session = Depends(get_db)):
    course = queries.get_course(db, course_id)
    if course is None:
        raise not_found()
    return course


@router.post('/', response_model=schemas.OneCourse, dependencies=[Depends(admin_only)])
def create_course(course: schemas.CreateCourse,
                  db: Session = Depends(get_db)):
    created_course = queries.create_course(db, course)
    return created_course


@router.delete('/{course_id}', status_code=204, dependencies=[Depends(admin_only)])
def delete_course(course_id: int,
                  db: Session = Depends(get_db)):
    course = queries.get_course(db, course_id)
    if course is None:
        raise not_found()

    queries.delete_course(db, course)
    return {}


@router.patch('/{course_id}', response_model=schemas.OneCourse, dependencies=[Depends(admin_only)])
def patch_course(course_id: int,
                 course: schemas.PatchCourse,
                 db: Session = Depends(get_db)):
    course_to_patch = queries.get_course(db, course_id)
    if course_to_patch is None:
        raise not_found()

    queries.patch_course(db, course_to_patch, course)

    return course_to_patch
