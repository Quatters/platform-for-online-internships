from datetime import datetime
from typing import List
from sqlalchemy import and_
from sqlalchemy.orm import Session
from backend.api.schemas.courses import Course
from backend.models.users import User
from backend.models.user_courses import UserCourse


def get_user_courses(db: Session, user_id: int) -> List[UserCourse]:
    return db.query(UserCourse).filter(UserCourse.user_id == user_id).all()


def get_user_course(db: Session, user_course_id: int) -> UserCourse | None:
    return db.query(UserCourse).get(user_course_id)


def get_user_course_by_course_id(db: Session,
                                 course_id: int,
                                 user_id: int) -> UserCourse | None:
    return db.query(UserCourse)\
             .filter(and_(UserCourse.user_id == user_id,
                          UserCourse.course_id == course_id))\
             .one_or_none()


def create_user_course(db: Session, user: User, course: Course) -> UserCourse:
    course = UserCourse(
            user_id=user.id,
            course_id=course.id,
            progress=0,
            admission_date=datetime.utcnow())

    db.add(course)
    db.commit()
    db.refresh(course)
    return course


def delete_user_course(db: Session, user_course: UserCourse):
    db.delete(user_course)
    db.commit()
