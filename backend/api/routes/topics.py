from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.api.auth import admin_only
from backend.api.current_dependencies import get_current_course, current_topic
from backend.api.dependencies import ListPageParams
from backend.api.errors.errors import not_found
from backend.api.schemas.courses import Course
from backend.database import get_db
from backend.api.queries import topics as queries
from backend.api.schemas import topics as schemas
from backend.models.topics import Topic
from backend.settings import LimitOffsetPage


router = APIRouter(prefix='/courses/{course_id}/topics')


@router.get('/',
            response_model=LimitOffsetPage[schemas.Topic])
def get_topics(params: ListPageParams = Depends(),
               course: Course = Depends(get_current_course),
               db: Session = Depends(get_db)):
    return queries.get_topics(db, params, course.id)


@router.get('/{topic_id}', response_model=schemas.OneTopic)
def get_topic(topic: Topic = Depends(current_topic)):
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
