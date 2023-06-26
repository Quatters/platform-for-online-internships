from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from backend.api.errors.errors import bad_request
from backend.constants import UserAnswerStatus
from backend.database import get_db
from backend.models import UserAnswer, User
from backend.api.auth import teacher_only
from backend.api.schemas import reviews as schemas
from backend.api.queries import reviews as queries
from backend.api.dependencies import ReviewListPageParams
from backend.api.current_dependencies import current_review
from backend.settings import LimitOffsetPage


router = APIRouter(prefix='/reviews')


@router.get('/', response_model=LimitOffsetPage[schemas.ListReview])
def get_reviews(
    params: ReviewListPageParams = Depends(),
    teacher: User = Depends(teacher_only),
    db: Session = Depends(get_db),
):
    return queries.get_reviews(db, teacher, params)


@router.get('/{review_id}', response_model=schemas.Review)
def get_one_review(review: UserAnswer = Depends(current_review)):
    return review


@router.put('/{review_id}', response_model=schemas.Review)
def finish_review(
    background_tasks: BackgroundTasks,
    data: schemas.FinishReview,
    review: UserAnswer = Depends(current_review),
    db: Session = Depends(get_db),
):
    if review.status is UserAnswerStatus.checked:
        raise bad_request('Review is already finished.')
    return queries.finish_review(db, review, data, background_tasks)
