from typing import List
from sqlalchemy.orm import Session
from backend.api.schemas import user_courses as schemas
from backend.models.user_courses import UserCourse


def get_courses(db: Session, user_id: int) -> List[UserCourse]:
    return db.query(UserCourse).filter(UserCourse.user_id == user_id).all()


def get_course(db: Session, user_course_id: int) -> UserCourse | None:
    return db.query(UserCourse).get(user_course_id)


def create_course(db: Session, user_id: int, course: schemas.CreateCourse) -> UserCourse:
    course = UserCourse(
            user_id=user_id,
            course_id=course.course_id)

    db.add(course)
    db.commit()
    db.refresh(course)
    return course


def delete_course(db: Session, user_course: UserCourse):
    db.delete(user_course)
    db.commit()
