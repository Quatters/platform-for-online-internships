import logging
import traceback
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from backend.models import TestAttempt, Task, Answer
from backend.api.schemas.test_attempts import UserAnswer
from backend.api.queries.answers import get_answer
from backend.api.queries.tasks import get_task
from backend.constants import TestAttemptStatus


logger = logging.getLogger(__file__)


def _handle_single_task(db: Session, task: Task, answer: Answer) -> tuple[int, int]:
    assert answer.id in {a.id for a in task.answers}
    return int(answer.is_correct), 1


def _handle_multiple_task(db: Session, task: Task, answer: list[Answer]) -> tuple[int, int]:
    user_answer_ids_set = set(a.id for a in answer)
    assert user_answer_ids_set.issubset(set(a.id for a in task.answers))

    user_score = max_score = 0
    for a in task.answers:
        max_score += int(a.is_correct)
        user_score += int(a.is_correct and a.id in user_answer_ids_set)

    return user_score, max_score


def _handle_text_task(db: Session, task: Task, answer: str) -> tuple[int, int]:
    return 0, 5


def finish_test(db: Session, test: TestAttempt, answers: list[UserAnswer]):
    assert test.status is TestAttemptStatus.in_progress

    test.finished_at = datetime.now()
    test.status = TestAttemptStatus.system_checking
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

                user_score, max_score = handler(db, task, answer)
                test.score += user_score
                test.max_score += max_score

        except:
            test.status = TestAttemptStatus.check_failure
            logger.error(traceback.format_exc())

    db.commit()
