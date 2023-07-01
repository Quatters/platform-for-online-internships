import logging
import traceback
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from backend.models import TestAttempt, Task, Answer, UserAnswer
from backend.api.schemas.test_attempts import UserAnswer as UserAnswerSchema
from backend.api.queries.answers import get_answer
from backend.api.queries.tasks import get_task
from backend.api.queries.user_courses import get_user_course_by_test_attempt, update_user_course_progress
from backend.constants import TaskType, TestAttemptStatus, UserAnswerStatus


logger = logging.getLogger(__file__)


def _handle_single_task(db: Session, task: Task, answer: Answer, attempt: TestAttempt) -> UserAnswer:
    assert answer.id in {a.id for a in task.answers}
    return UserAnswer(
        value=answer.value,
        user_id=attempt.user_id,
        attempt_id=attempt.id,
        task_type=task.task_type,
        task_name=task.name,
        task_description=task.description,
        status=UserAnswerStatus.checked,
        max_score=1,
        score=int(answer.is_correct),
    )


def _handle_multiple_task(db: Session, task: Task, answer: list[Answer], attempt: TestAttempt) -> UserAnswer:
    user_answer_ids_set = set(a.id for a in answer)
    assert user_answer_ids_set.issubset(set(a.id for a in task.answers))

    correct_answers_query = db.query(Answer).filter(
        (Answer.task_id == task.id) & (Answer.is_correct)
    )
    correct_answers_count = correct_answers_query.count()
    user_correct_answers_count = correct_answers_query.filter(Answer.id.in_(user_answer_ids_set)).count()

    score = 0
    if correct_answers_count == user_correct_answers_count:
        score = 2
    elif user_correct_answers_count / correct_answers_count >= 0.5:
        score = 1

    return UserAnswer(
        value=[a.value for a in answer],
        user_id=attempt.user_id,
        attempt_id=attempt.id,
        task_type=task.task_type,
        task_name=task.name,
        task_description=task.description,
        status=UserAnswerStatus.checked,
        max_score=2,
        score=score,
    )


def _handle_text_task(db: Session, task: Task, answer: str, attempt: TestAttempt) -> UserAnswer:
    return UserAnswer(
        value=answer,
        user_id=attempt.user_id,
        attempt_id=attempt.id,
        task_type=task.task_type,
        task_name=task.name,
        task_description=task.description,
        status=UserAnswerStatus.unchecked,
        max_score=5,
        score=0,
    )


def _calculate_max_score(db: Session, test: TestAttempt) -> int:
    tasks_query = db.query(Task).filter(Task.topic_id == test.topic_id)

    single_count = tasks_query.filter(Task.task_type == TaskType.single).count()
    multiple_count = tasks_query.filter(Task.task_type == TaskType.multiple).count()
    text_count = tasks_query.filter(Task.task_type == TaskType.text).count()

    return single_count + multiple_count * 2 + text_count * 5


def finish_test(db: Session, test: TestAttempt, answers: list[UserAnswerSchema]):
    assert test.status is TestAttemptStatus.in_progress

    test.finished_at = datetime.now()
    test.status = TestAttemptStatus.system_checking
    test.max_score = _calculate_max_score(db, test)
    db.commit()

    if test.finished_at > test.started_at + timedelta(seconds=test.time_to_pass):
        test.status = TestAttemptStatus.timeout_failure

    else:
        test.status = TestAttemptStatus.checked
        user_answers_to_create: list[UserAnswer] = []
        try:
            for user_answer in answers:
                task = get_task(db, user_answer.task_id)
                handler = None
                answer = None

                if task.task_type is TaskType.single:
                    handler = _handle_single_task
                    answer = get_answer(db, user_answer.answer)

                elif task.task_type is TaskType.multiple:
                    handler = _handle_multiple_task
                    answer = db.query(Answer).filter(Answer.id.in_(user_answer.answer)).all()

                elif task.task_type is TaskType.text:
                    handler = _handle_text_task
                    answer = user_answer.answer
                    test.status = TestAttemptStatus.partially_checked

                else:
                    raise ValueError(f'Invalid answer: {user_answer.answer}')

                created_user_answer: UserAnswer = handler(db, task, answer, test)
                user_answers_to_create.append(created_user_answer)
                test.score += created_user_answer.score

            db.bulk_save_objects(user_answers_to_create)

        except:  # nocv # noqa: E722
            test.status = TestAttemptStatus.check_failure
            logger.error(traceback.format_exc())

    db.commit()

    user_course = get_user_course_by_test_attempt(db, test)
    update_user_course_progress(db, user_course)
