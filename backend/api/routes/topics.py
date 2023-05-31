from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.api.auth import get_current_user
from backend.api.current_dependencies import current_course, current_topic
from backend.api.dependencies import ListPageParams
from backend.api.errors.errors import not_found, unauthorized
from backend.api.schemas.courses import Course
from backend.api.schemas.users import User
from backend.database import get_db
from backend.api.queries import topics as queries
from backend.api.schemas import topics as schemas
from backend.models.topics import Topic
from backend.settings import LimitOffsetPage


router = APIRouter(prefix='/courses/{course_id}/topics')


def populate_next_topic(topic: Topic, db: Session) -> schemas.OneTopic:
    topic.next_topic = queries.get_next_topic(db, topic.id)
    return schemas.OneTopic.from_orm(topic)


@router.get('/',
            response_model=LimitOffsetPage[schemas.Topic])
def get_topics(params: ListPageParams = Depends(),
               course: Course = Depends(current_course),
               db: Session = Depends(get_db)):
    return queries.get_topics(db, params, course.id)


@router.get('/{topic_id}', response_model=schemas.OneTopic)
def get_topic(topic: Topic = Depends(current_topic),
              db: Session = Depends(get_db)):
    return populate_next_topic(topic, db)


@router.post('/', response_model=schemas.OneTopic)
def create_topic(topic: schemas.CreateTopic,
                 course: Course = Depends(current_course),
                 user: User = Depends(get_current_user),
                 db: Session = Depends(get_db)):
    if not user.is_admin:
        raise unauthorized()

    if topic.prev_topic_id is not None:
        if queries.get_topic(db, topic.prev_topic_id) is None:
            raise not_found()

    created_topic = queries.create_topic(db, topic, course.id)
    return populate_next_topic(created_topic, db)


@router.delete('/{topic_id}', status_code=204)
def delete_topic(topic: Topic = Depends(current_topic),
                 user: User = Depends(get_current_user),
                 db: Session = Depends(get_db)):
    if not user.is_admin:
        raise unauthorized()
    queries.delete_topic(db, topic)
    return {}


@router.patch('/{topic_id}', response_model=schemas.OneTopic)
def patch_topic(topic: schemas.PatchTopic,
                topic_to_patch: Topic = Depends(current_topic),
                user: User = Depends(get_current_user),
                db: Session = Depends(get_db)):
    if not user.is_admin:
        raise unauthorized()
    queries.patch_topic(db, topic_to_patch, topic)
    return populate_next_topic(topic_to_patch, db)
