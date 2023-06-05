from datetime import datetime
from fastapi_pagination import paginate
from sqlalchemy import and_, func
from sqlalchemy.orm import Session, joinedload
from backend.api.schemas.courses import Course
from backend.models.users import User
from backend.models.user_courses import UserCourse
from backend.models.courses import Course as CourseModel
from backend.api.dependencies import ListPageParams


def get_user_courses(
    db: Session,
    user_id: int,
    params: ListPageParams,
):
    query = db.query(UserCourse) \
        .filter(UserCourse.user_id == user_id) \
        .options(
            joinedload(UserCourse.course, innerjoin=True).load_only(CourseModel.name)
        )

    if s := params.search:
        query = query.filter(
            UserCourse.course.has(func.lower(CourseModel.name).like(f'%{s}%'))
        )

    objects = query \
        .limit(params.limit) \
        .offset(params.offset) \
        .all()

    for obj in objects:
        obj.course_name = obj.course.name

    return paginate(
        objects,
        params,
        length_function=lambda _: query.count(),
    )


def get_user_course(db: Session, user_course_id: int) -> UserCourse | None:
    return db.query(UserCourse).get(user_course_id)


def get_user_course_by_course_id(db: Session,
                                 course_id: int,
                                 user_id: int) -> UserCourse | None:
    user_course = db.query(UserCourse).filter(and_(
        UserCourse.user_id == user_id,
        UserCourse.course_id == course_id)
    ).one_or_none()
    if user_course:
        user_course.course_name = user_course.course.name
        user_course.course_description = user_course.course.description
        user_course.posts = user_course.course.posts
        user_course.competencies = user_course.course.competencies
    return user_course


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
