from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.api.auth import get_current_user
from backend.api.errors.errors import bad_request, not_found, unauthorized
from backend.models.users import User
from backend.database import get_db
from backend.api.queries import courses, user_courses as queries
from backend.api.schemas import user_courses as schemas


router = APIRouter(prefix='/user/{user_id}/courses')


@router.get('/', response_model=list[schemas.UserCourse])
def get_user_courses(user_id: int,
                     user: User = Depends(get_current_user),
                     db: Session = Depends(get_db)):
    if user_id != user.id:
        raise unauthorized()
    return queries.get_user_courses(db, user_id)


@router.post('/', response_model=schemas.UserCourse)
def create_user_course(course_data: schemas.CreateCourse,
                       user_id: int,
                       user: User = Depends(get_current_user),
                       db: Session = Depends(get_db)):
    if user_id != user.id:
        raise unauthorized()
    if queries.get_user_course_by_course_id(db,
                                            user_id,
                                            course_data.course_id) is not None:
        raise bad_request("User is already registered for this course")
    course = courses.get_course(db, course_data.course_id)
    if course is None:
        raise not_found()
    return queries.create_user_course(db, user, course)


@router.delete('/{course_id}', status_code=204)
def delete_user_course(course_id: int,
                       user_id: int,
                       user: User = Depends(get_current_user),
                       db: Session = Depends(get_db)):
    if user_id != user.id:
        raise unauthorized()
    user_course = queries.get_user_course_by_course_id(db, course_id, user.id)
    if user_course is None:
        raise not_found()
    queries.delete_user_course(db, user_course)
    return {}
