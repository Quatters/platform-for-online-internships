from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.api.errors.errors import bad_request, not_found
from backend.database import get_db
from backend.api.queries import courses as queries
from backend.api.schemas import courses as schemas


router = APIRouter(prefix='/course')


@router.get('/', response_model=list[schemas.Course])
def get_courses(db: Session = Depends(get_db)):
    return queries.get_courses(db)


@router.get('/{course_id}', response_model=schemas.OneCourse)
def get_course(course_id: int, db: Session = Depends(get_db)):
    course = queries.get_course(db, course_id)
    if course is None:
        raise not_found()
    return course


@router.post('/', response_model=schemas.OneCourse)
def create_course(course: schemas.CreateCourse, db: Session = Depends(get_db)):
    if queries.get_course_by_name(db, course.name) is not None:
        raise bad_request('Course with the same name is already present in the database')
    created_course = queries.create_course(db, course)
    return created_course


@router.delete('/{course_id}', status_code=204)
def delete_course(course_id: int, db: Session = Depends(get_db)):
    course = queries.get_course(db, course_id)
    if course is None:
        raise not_found()

    queries.delete_course(db, course)
    return {}


@router.patch('/{course_id}', response_model=schemas.OneCourse)
def patch_course(course_id: int, course: schemas.PatchCourse, db: Session = Depends(get_db)):
    course_to_patch = queries.get_course(db, course_id)
    if course_to_patch is None:
        raise not_found()

    queries.patch_course(db, course_to_patch, course)

    return course_to_patch
