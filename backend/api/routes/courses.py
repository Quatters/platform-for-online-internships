from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.api.queries import courses as queries
from backend.api.schemas import courses as schemas


router = APIRouter(prefix='/courses')


@router.get('/', response_model=list[schemas.Course])
def get_courses(db: Session = Depends(get_db)):
    return queries.get_courses(db)


@router.get('/{course_id}', response_model=schemas.OneCourse)
def get_course(course_id: int, db: Session = Depends(get_db)):
    course = queries.get_course(db, course_id)
    if course is None:
        raise HTTPException(404, 'Not found.')  # probably need to wrap raising 404 as function
    return course


@router.post('/', response_model=schemas.OneCourse)
def create_course(course: schemas.CreateCourse, db: Session = Depends(get_db)):
    return queries.create_course(db, course)
