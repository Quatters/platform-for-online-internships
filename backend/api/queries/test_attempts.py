from sqlalchemy.orm import Session, joinedload
from fastapi_pagination import paginate as pypaginate
from backend.api.dependencies import ListPageParams
from backend.models import TestAttempt, Topic, Course
from backend.api.queries.helpers import sort_by_self_fk, with_search
from backend.api.schemas import test_attempts as schemas
from backend.constants import TestAttemptStatus


def get_test_by_id(db: Session, test_id: int) -> TestAttempt | None:
    return db.query(TestAttempt).get(test_id)


def get_going_test(db: Session, user_id: int):
    return db.query(TestAttempt).filter(
        (TestAttempt.user_id == user_id) & (TestAttempt.finished_at == None)  # noqa: E711
    ).one_or_none()


def get_user_tests(db: Session, params: ListPageParams, user_id: int):
    query = db.query(TestAttempt).filter(TestAttempt.user_id == user_id).options(
        joinedload(TestAttempt.topic).options(
            joinedload(Topic.course).load_only(Course.id, Course.name),
        ).load_only(Topic.id, Topic.name),
    ).order_by(TestAttempt.id.desc())
    query = with_search(TestAttempt.id, query=query, search=params.search)
    tests = query.all()

    for test in tests:
        test.course = schemas.Course(id=test.topic.course_id, name=test.topic.course.name)

    return pypaginate(tests, params, length_function=lambda _: query.count())


def create_test(db: Session, topic: Topic, user_id: int):
    time_to_pass = 0
    tasks = topic.tasks
    for task in tasks:
        time_to_pass += task.task_type.time_to_pass
        if task.task_type.may_have_answers():
            task.possible_answers = task.answers

    attempt = TestAttempt(
        user_id=user_id,
        topic_id=topic.id,
        time_to_pass=time_to_pass,
        status=TestAttemptStatus.in_progress,
    )
    db.add(attempt)
    db.commit()
    db.refresh(attempt)

    attempt.tasks = sort_by_self_fk(tasks, attr_='prev_task_id')

    return attempt
