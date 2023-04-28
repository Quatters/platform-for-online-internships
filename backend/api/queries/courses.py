from sqlalchemy.orm import Session
from backend.models import Course
from backend.api.schemas import courses as schemas


def get_courses(db: Session):
    return db.query(Course).all()


def get_course(db: Session, id: int) -> Course:
    return db.query(Course).get(id)


def create_course(db: Session, course: schemas.CreateCourse) -> Course:
    course = Course(**course.dict())
    db.add(course)
    db.commit()
    db.refresh(course)
    return course
