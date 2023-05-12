from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.api.auth import get_current_user
from backend.api.errors.errors import not_found, unathorized
from backend.api.schemas.users import User
from backend.database import get_db
from backend.api.queries import courses, topics as queries
from backend.api.schemas import topics as schemas


router = APIRouter(prefix='/courses/{course_id}/topics')


@router.get('/', response_model=list[schemas.OneTopic])
def get_topics(course_id: int,
               db: Session = Depends(get_db)):
    course = courses.get_course(db, course_id)
    if course is None:
        raise not_found()
    return queries.get_topics(db, course.id)

@router.get('/{topic_id}', response_model=schemas.Topic)
def get_topic(course_id: int,
              topic_id: int,
              db: Session = Depends(get_db)):
    course = courses.get_course(db, course_id)
    if course is None:
        raise not_found()
    topic = queries.get_topic(db, topic_id)
    if topic is None:
        raise not_found()
    return topic

@router.post('/', response_model=schemas.Topic)
def create_topic(course_id: int,
                 topic: schemas.CreateTopic,
                 user: User = Depends(get_current_user),
                 db: Session = Depends(get_db)):
    if not user.is_admin:
        raise unathorized()
    if courses.get_course(db, course_id) is None:
        raise not_found()

    created_topic = queries.create_topic(db, topic, course_id)
    return created_topic


@router.delete('/{topic_id}', status_code=204)
def delete_course(course_id: int,
                  topic_id: int,
                  user: User = Depends(get_current_user),
                  db: Session = Depends(get_db)):
    if not user.is_admin:
        raise unathorized()
    topic = queries.get_topic(db, topic_id)
    if topic is None:
        raise not_found()

    queries.delete_topic(db, topic)
    return {}


@router.patch('/{topic_id}', response_model=schemas.OneTopic)
def patch_course(course_id: int,
                 topic_id: int,
                 topic: schemas.PatchTopic,
                 user: User = Depends(get_current_user),
                 db: Session = Depends(get_db)):
    if not user.is_admin:
        raise unathorized()
    topic_to_patch = queries.get_topic(db, topic_id)
    if topic_to_patch is None:
        raise not_found()

    queries.patch_topic(db, topic_to_patch, topic)

    return topic_to_patch
