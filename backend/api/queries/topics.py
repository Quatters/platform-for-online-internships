from fastapi_pagination import paginate as pypaginate
from sqlalchemy.orm import Session
from backend.api.dependencies import ListPageParams
from backend.models.topics import Topic
from backend.api.schemas import topics as schemas
from backend.api.queries.helpers import sort_by_self_fk, with_search


def get_topics(db: Session, params: ListPageParams, course_id: int):
    query = db.query(Topic).filter(Topic.course_id == course_id)
    query = with_search(Topic.name, query=query, search=params.search)

    topics = sort_by_self_fk(query, 'prev_topic_id')
    return pypaginate(
        topics,
        params,
        length_function=lambda _: query.count(),
    )


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
