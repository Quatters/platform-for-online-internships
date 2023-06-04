from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.api.auth import admin_only
from backend.api.current_dependencies import current_topic, current_topic_resource
from backend.api.dependencies import ListPageParams
from backend.database import get_db
from backend.api.queries import topic_resources as queries
from backend.api.schemas import topic_resources as schemas
from backend.models.topics import Topic, TopicResource
from backend.settings import LimitOffsetPage


router = APIRouter(prefix='/courses/{course_id}/topics/{topic_id}/resources')


@router.get('/', response_model=LimitOffsetPage[schemas.ListTopicResource])
def get_resources(
    params: ListPageParams = Depends(),
    topic: Topic = Depends(current_topic),
    db: Session = Depends(get_db),
):
    return queries.get_topic_resources(db, params, topic.id)


@router.get(
    '/{resource_id}',
    response_model=schemas.OneTopicResource,
)
def get_one_resource(resource: TopicResource = Depends(current_topic_resource)):
    return resource


@router.post(
    '/',
    response_model=schemas.OneTopicResource,
    dependencies=[Depends(admin_only)],
)
def create_resource(
    resource: schemas.CreateTopicResource,
    topic: Topic = Depends(current_topic),
    db: Session = Depends(get_db),
):
    return queries.create_resource(db, resource, topic.id)


@router.patch(
    '/{resource_id}',
    response_model=schemas.OneTopicResource,
    dependencies=[Depends(admin_only)],
)
def patch_resource(
    resource_to_patch: schemas.PatchTopicResource,
    resource: TopicResource = Depends(current_topic_resource),
    db: Session = Depends(get_db),
):
    return queries.update_resource(db, resource, resource_to_patch)
