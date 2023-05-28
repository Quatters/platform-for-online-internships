from operator import attrgetter
from fastapi_pagination import paginate as pypaginate
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import func
from sqlalchemy.orm import Session
from backend.api.dependencies import ListPageParams
from backend.models.topics import Topic
from backend.api.schemas import topics as schemas


def get_topics(db: Session, params: ListPageParams):
    query = db.query(Topic)
    if s := params.search:
        query = query.filter(func.lower(Topic.name).like(f'%{s.lower()}%'))

    topics = query.all()

    if not topics:
        return pypaginate(topics, params)

    cur = None
    firsts = [item for item in topics if item.prev_topic_id is None]
    if firsts:
        cur = firsts[0]
    else:
        cur = min(topics, key=attrgetter('prev_topic_id'))

    result = [cur]
    topics.remove(cur)
    while len(topics) > 0:
        for obj in topics:
            if obj.prev_topic_id == cur.id:
                cur = obj
                result.append(cur)
                topics.remove(obj)

    return pypaginate(result, params, length_function=lambda _: query.count())


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
