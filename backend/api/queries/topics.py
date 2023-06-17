from functools import partial
from fastapi_pagination import paginate as pypaginate
from sqlalchemy.orm import Session
from backend.api.dependencies import ListPageParams
from backend.models.topics import Topic
from backend.api.schemas import topics as schemas
from backend.api.queries.helpers import (
    create_with_respect_to_prev_instance,
    delete_with_respect_to_prev_instance,
    update_with_respect_to_prev_instance,
    with_search,
    sort_by_self_fk,
)


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
    return db.get(Topic, topic_id)


def get_first_topic(db: Session, course_id: int):
    return db.query(Topic).filter(
        (Topic.prev_topic_id == None) & (Topic.course_id == course_id)  # noqa: E711
    ).one_or_none()


def create_topic(db: Session, topic: schemas.CreateTopic, course_id: int) -> Topic:
    return create_with_respect_to_prev_instance(
        db=db,
        create_data={**topic.dict(), 'course_id': course_id},
        prev_id_attr_name='prev_topic_id',
        next_instance_attr_name='next_topic',
        model=Topic,
        get_first_func=partial(get_first_topic, db, course_id),
        get_prev_func=partial(get_topic, db, topic.prev_topic_id),
    )


def delete_topic(db: Session, topic: Topic):
    delete_with_respect_to_prev_instance(
        db=db,
        instance=topic,
        prev_id_attr_name='prev_topic_id',
        next_instance_attr_name='next_topic',
    )


def patch_topic(db: Session, topic: Topic, data: schemas.PatchTopic) -> Topic:
    return update_with_respect_to_prev_instance(
        db=db,
        instance=topic,
        prev_id_attr_name='prev_topic_id',
        next_instance_attr_name='next_topic',
        update_data=data.dict(exclude_unset=True),
        additional_filters_to_search_for_instance_to_update=[
            Topic.course_id == topic.course_id,
        ]
    )
