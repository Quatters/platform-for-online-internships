from typing import List
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import and_, func
from sqlalchemy.orm import Session, query
from backend.api.dependencies import ListPageParams
from backend.models.topics import Topic
from backend.api.schemas import topics as schemas

def get_topics(db: Session, course_id: int, params: ListPageParams) -> List[Topic]:
    query = db.query(Topic).filter(Topic.course_id == course_id)
    if s := params.search:
        query = query.filter(func.lower(Topic.name).like(f'%{s.lower()}%'))
    return paginate(query, params)


def get_topic(db: Session, topic_id: int, course_id: int) -> Topic | None:
    return db.query(Topic).filter(and_(Topic.course_id == course_id, Topic.id == topic_id)).one_or_none()


def create_topic(db: Session, topic: schemas.CreateTopic, course_id: int) -> Topic:
    topic = Topic(**topic.dict())
    topic.course_id = course_id
    db.add(topic)
    db.commit()
    db.refresh(topic)
    return topic


def delete_topic(db: Session, topic: Topic):
    db.delete(topic)
    db.commit()


def patch_topic(db: Session, topic: Topic, data: schemas.PatchTopic) -> Topic:
    db.query(Topic).filter(Topic.id == topic.id).update(data.dict(exclude_unset=True))
    db.commit()
    db.refresh(topic)
    return topic
