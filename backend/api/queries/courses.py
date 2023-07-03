from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session
from backend.models import Course
from backend.api.schemas import courses as schemas
from backend.api.dependencies import ListPageParams
from backend.api.queries.helpers import get_instances_or_400, with_search
from backend.models.competencies import Competence
from backend.models.posts import Post
from backend.models.users import User


def get_courses(db: Session, params: ListPageParams):
    query = with_search(Course.name, query=db.query(Course), search=params.search)
    query = query.order_by(Course.name)
    return paginate(query, params)


def get_course(db: Session, id: int) -> Course | None:
    return db.get(Course, id)


def get_course_by_name(db: Session, name: str) -> Course | None:
    return db.query(Course).filter(Course.name == name).one_or_none()


def get_user_recommended_courses(user: User):
    def has_all_competencies(user: User, course: Course):
        return set(course.competencies).issubset(set(user.competencies))

    posts = user.posts
    print(user.posts)
    recommended_courses = []
    for post in posts:
        for course in post.courses:
            if not has_all_competencies(user, course):
                recommended_courses.append(course)

    def get_course_name(course: Course):
        return course.name

    recommended_courses.sort(key=get_course_name)
    return recommended_courses


def create_course(db: Session, course: schemas.CreateCourse) -> Course:
    created_course = Course(**course.dict(exclude={'competencies', 'posts'}))
    created_course.competencies = get_instances_or_400(db, Competence, course.competencies)
    created_course.posts = get_instances_or_400(db, Post, course.posts)
    db.add(created_course)
    db.commit()
    db.refresh(created_course)
    return created_course


def delete_course(db: Session, course: Course):
    db.delete(course)
    db.commit()


def patch_course(db: Session, course: Course, data: schemas.PatchCourse) -> Course:
    dict_ = data.dict(exclude_unset=True)
    if 'competencies' in dict_:
        course.competencies = get_instances_or_400(db, Competence, dict_.pop('competencies'))
    if 'posts' in dict_:
        course.posts = get_instances_or_400(db, Post, dict_.pop('posts'))
    for key, value in dict_.items():
        setattr(course, key, value)
    db.commit()
    db.refresh(course)
    return course
