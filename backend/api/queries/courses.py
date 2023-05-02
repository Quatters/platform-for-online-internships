from sqlalchemy.orm import Session
from backend.models import Course
from backend.api.schemas import courses as schemas


def get_courses(db: Session):
    return db.query(Course).all()


def get_course(db: Session, id: int) -> Course | None:
    return db.query(Course).get(id)


def get_course_by_name(db: Session, name: str) -> Course | None:
    return db.query(Course).filter(Course.name == name).one_or_none()


def create_course(db: Session, course: schemas.CreateCourse) -> Course:
    course = Course(**course.dict())
    db.add(course)
    db.commit()
    db.refresh(course)
    return course


def delete_course(db: Session, course: Course):
    db.delete(course)
    db.commit()


def patch_course(db: Session, course: Course, data: schemas.PatchCourse) -> Course:
    if data.name is not None:
        course.name = data.name
    if data.description is not None:
        course.description = data.description
    db.commit()
    db.refresh(course)
    return course
