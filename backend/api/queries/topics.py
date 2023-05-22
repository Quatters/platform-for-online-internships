from typing import List
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import func
from sqlalchemy.orm import Session
from backend.api.dependencies import ListPageParams
from backend.models.topics import Topic
from backend.api.schemas import topics as schemas


def get_topics(db: Session, params: ListPageParams) -> List[Topic]:
    query = db.query(Topic)
    if s := params.search:
        query = query.filter(func.lower(Topic.name).like(f'%{s.lower()}%'))
    vals = paginate(query, params)

    firsts = [item for item in vals.items if item.prev_topic_id is None]
    cur = firsts[0]

    result = [cur]
    vals.items.remove(cur)
    while len(vals.items) > 0:
        for obj in vals.items:
            if obj.prev_topic_id == cur.id:
                cur = obj
                result.append(cur)
                vals.items.remove(obj)

    vals.items = result
    return vals


def get_topic(db: Session, topic_id: int) -> Topic | None:
    return db.query(Topic).get(topic_id)


def get_next_topic(db: Session, topic_id: int) -> Topic | None:
    return db.query(Topic).filter(Topic.prev_topic_id == topic_id).one_or_none()


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
