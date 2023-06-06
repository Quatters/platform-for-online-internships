from sqlalchemy.orm import Session
from backend.models import TestAttempt, Topic
from backend.api.queries.helpers import sort_by_self_fk


def get_going_attempt(db: Session, user_id: int):
    return db.query(TestAttempt).filter(
        (TestAttempt.user_id == user_id) & (TestAttempt.ended_at == None)  # noqa: E711
    ).one_or_none()


def create_attempt(db: Session, topic: Topic, user_id: int):
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
    )
    db.add(attempt)
    db.commit()
    db.refresh(attempt)

    attempt.tasks = sort_by_self_fk(tasks, attr_='prev_task_id')

    return attempt
