from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.api.errors.errors import not_found
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
