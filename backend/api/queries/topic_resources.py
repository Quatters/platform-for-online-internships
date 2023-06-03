from functools import partial
from sqlalchemy.orm import Session
from fastapi_pagination import paginate as pypaginate
from backend.api.dependencies import ListPageParams
from backend.api.queries.helpers import create_with_respect_to_prev_instance, sort_by_self_fk, update_with_respect_to_prev_instance, with_search
from backend.models import TopicResource
from backend.api.schemas import topic_resources as schemas


def get_topic_resources(db: Session, params: ListPageParams, topic_id: int):
    query = db.query(TopicResource).filter(TopicResource.topic_id == topic_id)
    query = with_search(TopicResource.name, query=query, search=params.search)

    resources = sort_by_self_fk(query, 'prev_resource_id')
    return pypaginate(
        resources,
        params,
        length_function=lambda _: query.count(),
    )


def get_topic_resource(db: Session, resource_id: int) -> TopicResource | None:
    return db.query(TopicResource).get(resource_id)


def get_first_topic_resource(db: Session, topic_id: int) -> TopicResource | None:
    return db.query(TopicResource)\
        .filter((TopicResource.topic_id == topic_id) & (TopicResource.prev_resource_id == None))\
        .one_or_none()


def create_resource(db: Session, resource: schemas.CreateTopicResource, topic_id: int) -> TopicResource:
    return create_with_respect_to_prev_instance(
        db=db,
        create_data={**resource.dict(), 'topic_id': topic_id},
        prev_id_attr_name='prev_resource_id',
        next_instance_attr_name='next_resource',
        model=TopicResource,
        get_first_func=partial(get_first_topic_resource, db, topic_id),
        get_prev_func=partial(get_topic_resource, db, resource.prev_resource_id),
    )


def update_resource(db: Session, resource: TopicResource, update_data: schemas.PatchTopicResource):
    return update_with_respect_to_prev_instance(
        db=db,
        instance=resource,
        update_data=update_data.dict(exclude_unset=True),
        prev_id_attr_name='prev_resource_id',
        next_instance_attr_name='next_resource',
        additional_filters_to_search_for_instance_to_update=[
            TopicResource.topic_id == resource.topic_id,
        ]
    )
