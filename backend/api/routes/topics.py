from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.api.auth import admin_only, get_current_user
from backend.api.current_dependencies import get_current_course, current_topic
from backend.api.dependencies import ListPageParams
from backend.api.errors.errors import not_found
from backend.api.schemas.courses import Course
from backend.database import get_db
from backend.api.queries import topics as queries
from backend.api.schemas import topics as schemas
from backend.api.queries import test_attempts as test_attempts_queries
from backend.models import Topic, User
from backend.settings import LimitOffsetPage


router = APIRouter(prefix='/courses/{course_id}/topics')


@router.get('/',
            response_model=LimitOffsetPage[schemas.Topic])
def get_topics(params: ListPageParams = Depends(),
               course: Course = Depends(get_current_course),
               db: Session = Depends(get_db)):
    return queries.get_topics(db, params, course.id)


@router.get('/{topic_id}', response_model=schemas.OneTopic)
def get_topic(
    topic: Topic = Depends(current_topic),
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not user.is_admin and not user.is_teacher:
        topic.attempts_amount = max(
            topic.attempts_amount - test_attempts_queries.get_existing_attempts_count(db, user.id, topic.id),
            0
        )
    return topic


@router.post('/', response_model=schemas.OneTopic, dependencies=[Depends(admin_only)])
def create_topic(topic: schemas.CreateTopic,
                 course: Course = Depends(get_current_course),
                 db: Session = Depends(get_db)):
    if topic.prev_topic_id is not None:
        if queries.get_topic(db, topic.prev_topic_id) is None:
            raise not_found()

    return queries.create_topic(db, topic, course.id)


@router.delete('/{topic_id}', status_code=204, dependencies=[Depends(admin_only)])
def delete_topic(topic: Topic = Depends(current_topic),
                 db: Session = Depends(get_db)):
    queries.delete_topic(db, topic)
    return {}


@router.patch('/{topic_id}', response_model=schemas.OneTopic, dependencies=[Depends(admin_only)])
def patch_topic(topic: schemas.PatchTopic,
                topic_to_patch: Topic = Depends(current_topic),
                db: Session = Depends(get_db)):
    return queries.patch_topic(db, topic_to_patch, topic)
