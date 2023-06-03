from sqlalchemy.orm import Session
from fastapi_pagination import paginate as pypaginate
from backend.api.dependencies import ListPageParams
from backend.api.errors.errors import bad_request
from backend.api.queries.helpers import sort_by_self_fk, with_search
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
    after_add_callback = lambda _: None

    if resource.prev_resource_id is None:
        existing_first_resource = get_first_topic_resource(db, topic_id)
        if existing_first_resource is not None:

            def callback(created_resource):
                existing_first_resource.prev_resource_id = created_resource.id

            after_add_callback = callback
    else:
        existing_prev_resource = get_topic_resource(db, resource.prev_resource_id)
        if existing_prev_resource is None:
            raise bad_request(f'Resource with id {resource.prev_resource_id} does not exist.')

        def callback(created_resource):
            existing_prev_resource.next_resource.prev_resource_id = created_resource.id
            created_resource.prev_resource_id = existing_prev_resource.id

        after_add_callback = callback

    created_resource = TopicResource(
        **resource.dict(exclude={'prev_resource_id'}),
        topic_id=topic_id,
    )

    db.add(created_resource)
    db.commit()
    db.refresh(created_resource)

    after_add_callback(created_resource)
    db.commit()
    db.refresh(created_resource)

    return created_resource


def update_resource(db: Session, resource: TopicResource, update_data: schemas.PatchTopicResource):
    dict_ = update_data.dict(exclude_unset=True)

    after_update_callback = lambda *args, **kwargs: None
    resource_to_update = None

    if 'prev_resource_id' in dict_:
        updated_prev_resource_id = dict_.pop('prev_resource_id')
        if resource.prev_resource_id != updated_prev_resource_id:
            if resource.next_resource is not None:
                resource.next_resource.prev_resource_id = resource.prev_resource_id
            resource_to_update = db.query(TopicResource).filter(
                (TopicResource.topic_id == resource.topic_id)
                & (TopicResource.prev_resource_id == updated_prev_resource_id)
            ).one_or_none()
            resource.prev_resource_id = updated_prev_resource_id

            if resource_to_update is not None:
                resource_to_update.prev_resource_id = None

                def callback(resource_to_update, prev_resource_id):
                    resource_to_update.prev_resource_id = prev_resource_id

                after_update_callback = callback

    for key, value in dict_.items():
        setattr(resource, key, value)

    db.commit()
    db.refresh(resource)

    after_update_callback(resource_to_update, resource.id)
    db.commit()

    return resource
