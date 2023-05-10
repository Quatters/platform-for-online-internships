from typing import List
from sqlalchemy.orm import Session
from backend.models.topics import Topic


def get_topics(db: Session, course_id: int) -> List[Topic]:
    return db.query(Topic).filter(Topic.course_id == course_id).all()


def get_topic(db: Session, topic_id: int) -> Topic | None:
    return db.query(Topic).get(topic_id)
