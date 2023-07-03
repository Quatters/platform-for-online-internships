from sqlalchemy.orm import Session, joinedload
from fastapi_pagination import paginate as pypaginate
from backend.api.dependencies import TestAttemptListPageParams
from backend.models import TestAttempt, Topic, Course, UserCourse, User
from backend.api.queries.helpers import sort_by_self_fk, with_search
from backend.api.schemas import test_attempts as schemas
from backend.constants import TestAttemptStatus


def get_test_by_id(db: Session, test_id: int) -> TestAttempt | None:
    return db.get(TestAttempt, test_id)


def get_going_test(db: Session, user_id: int):
    return db.query(TestAttempt).filter(
        TestAttempt.user_id == user_id,
        TestAttempt.finished_at == None,  # noqa: E711
    ).one_or_none()


def get_existing_attempts_count(db: Session, user: User, topic: Topic, user_course: UserCourse):
    return db.query(TestAttempt).filter(
        TestAttempt.user_id == user.id,
        TestAttempt.topic_id == topic.id,
        TestAttempt.user_course_id == user_course.id,
    ).count()


def get_going_test_with_tasks(db: Session, user_id: int) -> TestAttempt | None:
    test = get_going_test(db, user_id)
    if not test:
        return test

    tasks = test.topic.tasks
    for task in tasks:
        if task.task_type.may_have_answers():
            task.possible_answers = task.answers

    test.tasks = sort_by_self_fk(tasks, attr_='prev_task_id')
    return test


def get_user_tests(db: Session, params: TestAttemptListPageParams, user_id: int):
    query = db.query(TestAttempt).filter(TestAttempt.user_id == user_id).options(
        joinedload(TestAttempt.topic).options(
            joinedload(Topic.course).load_only(Course.id, Course.name),
        ).load_only(Topic.id, Topic.name),
    ).order_by(TestAttempt.id.desc())
    if params.status is not None:
        query = query.filter(TestAttempt.status == params.status)
    query = with_search(TestAttempt.id, query=query, search=params.search)
    tests = query.all()

    for test in tests:
        test.course = schemas.Course(id=test.topic.course_id, name=test.topic.course.name)

    return pypaginate(tests, params, length_function=lambda _: query.count())


def create_test(db: Session, topic: Topic, user: User, user_course: UserCourse):
    time_to_pass = 0
    tasks = topic.tasks
    for task in tasks:
        time_to_pass += task.task_type.time_to_pass
        if task.task_type.may_have_answers():
            task.possible_answers = task.answers

    test = TestAttempt(
        user_id=user.id,
        topic_id=topic.id,
        user_course_id=user_course.id,
        time_to_pass=time_to_pass,
        status=TestAttemptStatus.in_progress,
    )
    db.add(test)
    db.commit()
    db.refresh(test)

    test.tasks = tasks

    return test
