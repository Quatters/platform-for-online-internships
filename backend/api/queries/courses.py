from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session
from backend.models import Course, Post, Competence, User
from backend.models.association_tables import CourseCompetenceAssociation, CoursePostAssociation, UserPostAssociation
from backend.api.schemas import courses as schemas
from backend.api.dependencies import ListPageParams, RecommendedCoursesListPageParams
from backend.api.queries.helpers import get_instances_or_400, with_search


def get_courses(db: Session, params: ListPageParams):
    query = with_search(Course.name, query=db.query(Course), search=params.search)
    query = query.order_by(Course.name)
    return paginate(query, params)


def get_recommended_courses(db: Session, intern: User, params: RecommendedCoursesListPageParams):
    post_ids_query = db.query(UserPostAssociation.c.post_id).filter(
        UserPostAssociation.c.user_id == intern.id,
    )
    if params.post_id:
        post_ids_query = post_ids_query.filter(UserPostAssociation.c.post_id == params.post_id)
    course_ids_query = db.query(CoursePostAssociation.c.course_id).filter(
        CoursePostAssociation.c.post_id.in_(post_ids_query),
    )
    intern_competencies_ids = intern.competencies_ids
    suitable_by_competencies_course_ids_query = db.query(CourseCompetenceAssociation.c.course_id).filter(
        ~(CourseCompetenceAssociation.c.competence_id.in_(intern_competencies_ids))
    )
    course_ids_query = course_ids_query.filter(
        CoursePostAssociation.c.course_id.in_(suitable_by_competencies_course_ids_query),
    )
    courses_query = db.query(Course).filter(
        Course.id.in_(course_ids_query),
    ).order_by(
        Course.name,
    )
    course_query = with_search(Course.name, query=courses_query, search=params.search)
    return paginate(course_query, params)


def get_course(db: Session, id: int) -> Course | None:
    return db.get(Course, id)


def get_course_by_name(db: Session, name: str) -> Course | None:
    return db.query(Course).filter(Course.name == name).one_or_none()


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
