from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.api.auth import get_current_user
from backend.api.current_dependencies import current_course, current_topic
from backend.api.dependencies import ListPageParams
from backend.api.errors.errors import not_found, unauthorized
from backend.api.schemas.courses import Course
from backend.api.schemas.users import User
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
