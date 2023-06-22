from fastapi import BackgroundTasks
from sqlalchemy.orm import Session
from fastapi_pagination.ext.sqlalchemy import paginate
from backend.api.dependencies import ReviewListPageParams
from backend.api.queries.helpers import with_search
from backend.api.queries.user_courses import update_user_course_progress, get_user_course_by_course_id
from backend.models import User, UserAnswer
from backend.constants import TaskType, TestAttemptStatus, UserAnswerStatus
from backend.api.schemas import reviews as schemas


def get_reviews(db: Session, teacher: User, params: ReviewListPageParams):
    query = db.query(UserAnswer).filter(
        UserAnswer.task_type == TaskType.text,
        UserAnswer.user_id.in_(db.query(User.id).filter(User.teacher_id == teacher.id)),
    )
    if params.status is not None:
        query = query.filter(UserAnswer.status == params.status)
    query = with_search(UserAnswer.task_name, query=query, search=params.search)
    return paginate(query, params)


def get_review(db: Session, user_answer_id: int) -> UserAnswer | None:
    return db.query(UserAnswer).filter(
        UserAnswer.task_type == TaskType.text,
        UserAnswer.id == user_answer_id,
    ).one_or_none()


def finish_review(
    db: Session,
    user_answer: UserAnswer,
    data: schemas.FinishReview,
    background_tasks: BackgroundTasks,
):
    user_answer.status = UserAnswerStatus.checked
    user_answer.score = data.score
    user_answer.review = data.review
    user_answer.attempt.score += data.score

    unchecked_answers_count = db.query(UserAnswer).filter(
        UserAnswer.id != user_answer.id,
        UserAnswer.status == UserAnswerStatus.unchecked,
    ).count()
    if unchecked_answers_count == 0:
        user_answer.attempt.status = TestAttemptStatus.checked

    db.commit()

    user_course = get_user_course_by_course_id(db, user_answer.attempt.topic.course_id, user_answer.user_id)
    background_tasks.add_task(update_user_course_progress, db, user_course)

    db.refresh(user_answer)
    return user_answer
