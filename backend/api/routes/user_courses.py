from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.api.errors.errors import bad_request, not_found
from backend.database import get_db
from backend.api.queries import user_courses as queries
from backend.api.schemas import user_courses as schemas


router = APIRouter(prefix='/user/{user_id}/courses')


@router.get('/', response_model=list[schemas.UserCourse])
def get_courses(user_id: int, db: Session = Depends(get_db)):
    return queries.get_courses(db, user_id)


@router.post('/', response_model=schemas.UserCourse)
def create_user_course(user_id: int, course: schemas.CreateCourse, db: Session = Depends(get_db)):
    return queries.create_course(db, user_id, course)


@router.delete('/{user_course_id}', status_code=204)
def delete_user_course(user_course_id: int, db: Session = Depends(get_db)):
    course = queries.get_course(db, user_course_id)
    if course is None:
        raise not_found()

    queries.delete_course(db, course)
    return {}
