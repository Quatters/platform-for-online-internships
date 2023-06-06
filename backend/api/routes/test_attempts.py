from fastapi import APIRouter, Depends
from fastapi.background import BackgroundTasks
from sqlalchemy.orm import Session
from backend.api.auth import intern_only
from backend.api.errors.errors import bad_request, not_found
from backend.api.schemas import test_attempts as schemas
from backend.api.queries import test_attempts as queries
from backend.api.current_dependencies import current_topic
from backend.database import get_db
from backend.models import Topic, User
from backend.models.test_attempts import TestAttempt
from backend.api.dependencies import ListPageParams
from backend.api.background_tasks import test_attempts as tasks
from backend.settings import LimitOffsetPage


router = APIRouter()


def current_test(test_id: int, user: User = Depends(intern_only), db: Session = Depends(get_db)):
    test = queries.get_test_by_id(db, test_id)
    if test is None or test.user_id != user.id:
        raise not_found()
    return test


@router.post('/courses/{course_id}/topics/{topic_id}/start_test', response_model=schemas.GoingTest)
def start_test(
    topic: Topic = Depends(current_topic),
    user: User = Depends(intern_only),
    db: Session = Depends(get_db),
):
    going_test = queries.get_going_test(db, user.id)
    if going_test is not None:
        raise bad_request('Cannot start new test until there is unfinished one.')

    return queries.create_test(db, topic, user.id)


@router.post(
    '/tests/{test_id}/finish',
    response_model=schemas.FinishTestResponse,
    dependencies=[Depends(intern_only)],
)
def finish_test(
    background_tasks: BackgroundTasks,
    user_answers: list[schemas.UserAnswer],
    test: TestAttempt = Depends(current_test),
    db: Session = Depends(get_db),
):
    background_tasks.add_task(tasks.finish_test, test=test, answers=user_answers, db=db)
    return schemas.FinishTestResponse()


@router.get('/tests/going', response_model=schemas.GoingTest | None)
def get_going_test(
    user: User = Depends(intern_only),
    db: Session = Depends(get_db),
):
    return queries.get_going_test_with_tasks(db, user.id)


@router.get('/tests/{test_id}', response_model=schemas.OneTest, dependencies=[Depends(intern_only)])
def get_one_user_test(test: TestAttempt = Depends(current_test)):
    test.course = {
        'id': test.topic.course_id,
        'name': test.topic.course.name,
    }
    return test


@router.get('/tests', response_model=LimitOffsetPage[schemas.ListTest])
def get_user_tests(
    params: ListPageParams = Depends(),
    user: User = Depends(intern_only),
    db: Session = Depends(get_db),
):
    return queries.get_user_tests(db, params, user.id)
