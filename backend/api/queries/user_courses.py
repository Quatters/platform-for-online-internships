from datetime import datetime
from fastapi_pagination import paginate
from sqlalchemy import func, select
from sqlalchemy.orm import Session, joinedload
from backend.models import UserCourse, TestAttempt, User, Course, Task, Topic, UserCompetence
from backend.models.courses import Course as CourseModel
from backend.api.dependencies import ListPageParams
from backend.constants import TaskType


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
        obj.pass_percent = obj.course.pass_percent

    return paginate(
        objects,
        params,
        length_function=lambda _: query.count(),
    )


def get_user_course_by_course_id(db: Session,
                                 course_id: int,
                                 user_id: int) -> UserCourse | None:
    return db.query(UserCourse).filter(
        UserCourse.user_id == user_id,
        UserCourse.course_id == course_id,
    ).one_or_none()


def get_annotated_user_course_by_course_id(
    db: Session,
    course_id: int,
    user_id: int,
) -> UserCourse | None:
    user_course = get_user_course_by_course_id(db, course_id, user_id)
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


def _calculate_max_course_score(db: Session, course: Course):
    all_task_ids_query = db.query(Task.id).filter(Task.topic_id.in_(
        db.query(Topic.id).filter(Topic.course_id == course.id)
    ))
    single_tasks_count = all_task_ids_query.filter(Task.task_type == TaskType.single).count()
    multiple_tasks_count = all_task_ids_query.filter(Task.task_type == TaskType.multiple).count()
    text_tasks_count = all_task_ids_query.filter(Task.task_type == TaskType.text).count()
    return (
        single_tasks_count
        + multiple_tasks_count * 2
        + text_tasks_count * 5
    )


def _calculate_user_course_score(db: Session, user_course: UserCourse):
    topic_ids_query = select(Topic.id).where(
        Topic.course_id == user_course.course_id,
    )
    best_attempts_query = select(
        func.max(TestAttempt.score).label('best_score')
    ).where(
        TestAttempt.topic_id.in_(topic_ids_query),
        TestAttempt.user_id == user_course.user_id,
    ).group_by(
        TestAttempt.user_id,
        TestAttempt.topic_id,
    )
    sum_query = select(
        func.sum(best_attempts_query.subquery().c.best_score)
    )
    return db.scalar(sum_query)


def _calculate_user_course_progress(db: Session, user_course: UserCourse):
    progress = 0
    try:
        progress = (
            _calculate_user_course_score(db, user_course)
            / _calculate_max_course_score(db, user_course.course)
            * 100
        )
    except ZeroDivisionError:  # nocv
        pass
    return progress


def update_user_course_progress(db: Session, user_course: UserCourse):
    prev_progress = user_course.progress
    user_course.progress = _calculate_user_course_progress(db, user_course)
    if user_course.progress >= user_course.course.pass_percent and prev_progress < user_course.course.pass_percent:
        for competence in user_course.course.competencies:
            if competence.id not in user_course.user.competencies_ids:
                user_course.user.user_competencies.append(UserCompetence(
                    user_id=user_course.user_id,
                    competence_id=competence.id,
                ))
    db.commit()


def get_user_course_by_test_attempt(db: Session, test_attempt: TestAttempt):
    return db.scalar(select(UserCourse).where(
        UserCourse.user_id == test_attempt.user_id,
        UserCourse.course_id == test_attempt.topic.course_id,
    ))
