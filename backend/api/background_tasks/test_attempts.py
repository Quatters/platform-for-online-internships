import logging
import traceback
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from backend.models import TestAttempt, Task, Answer
from backend.api.schemas.test_attempts import UserAnswer
from backend.api.queries.answers import get_answer
from backend.api.queries.tasks import get_task
from backend.constants import TaskType, TestAttemptStatus


logger = logging.getLogger(__file__)


def _handle_single_task(db: Session, task: Task, answer: Answer) -> int:
    assert answer.id in {a.id for a in task.answers}
    return int(answer.is_correct)


def _handle_multiple_task(db: Session, task: Task, answer: list[Answer]) -> int:
    user_answer_ids_set = set(a.id for a in answer)
    assert user_answer_ids_set.issubset(set(a.id for a in task.answers))

    correct_answers_query = db.query(Answer).filter(
        (Answer.task_id == task.id) & (Answer.is_correct)
    )
    correct_answers_count = correct_answers_query.count()
    user_correct_answers_count = correct_answers_query.filter(Answer.id.in_(user_answer_ids_set)).count()

    if correct_answers_count == user_correct_answers_count:
        return 2
    if user_correct_answers_count / correct_answers_count >= 0.5:
        return 1
    return 0


def _handle_text_task(db: Session, task: Task, answer: str) -> int:
    return 0


def _calculate_max_score(db: Session, test: TestAttempt) -> int:
    tasks_query = db.query(Task).filter(Task.topic_id == test.topic_id)

    single_count = tasks_query.filter(Task.task_type == TaskType.single).count()
    multiple_count = tasks_query.filter(Task.task_type == TaskType.multiple).count()
    text_count = tasks_query.filter(Task.task_type == TaskType.text).count()

    return single_count + multiple_count * 2 + text_count * 5


def finish_test(db: Session, test: TestAttempt, answers: list[UserAnswer]):
    assert test.status is TestAttemptStatus.in_progress

    test.finished_at = datetime.now()
    test.status = TestAttemptStatus.system_checking
    test.max_score = _calculate_max_score(db, test)
    db.commit()

    if test.finished_at > test.started_at + timedelta(seconds=test.time_to_pass):
        test.status = TestAttemptStatus.timeout_failure

    else:
        test.status = TestAttemptStatus.checked
        try:
            for user_answer in answers:
                task = get_task(db, user_answer.task_id)
                handler = None
                answer = None

                if isinstance(user_answer.answer, int):
                    handler = _handle_single_task
                    answer = get_answer(db, user_answer.answer)

                elif isinstance(user_answer.answer, list):
                    handler = _handle_multiple_task
                    answer = db.query(Answer).filter(Answer.id.in_(user_answer.answer)).all()

                elif isinstance(user_answer.answer, str):
                    handler = _handle_text_task
                    answer = user_answer.answer
                    test.status = TestAttemptStatus.partially_checked

                else:
                    raise ValueError(f'Invalid answer: {user_answer.answer}')

                test.score += handler(db, task, answer)

        except:  # noqa: E722
            test.status = TestAttemptStatus.check_failure
            logger.error(traceback.format_exc())

    db.commit()
