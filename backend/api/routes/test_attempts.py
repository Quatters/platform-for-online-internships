from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.api.auth import intern_only
from backend.api.errors.errors import bad_request
from backend.api.schemas import test_attempts as schemas
from backend.api.queries import test_attempts as queries
from backend.api.current_dependencies import current_topic
from backend.database import get_db
from backend.models import Topic, User


router = APIRouter(prefix='/courses/{course_id}/topics/{topic_id}')


@router.post('/make_test', response_model=schemas.NewTest)
def make_test(
    topic: Topic = Depends(current_topic),
    user: User = Depends(intern_only),
    db: Session = Depends(get_db),
):
    going_attempt = queries.get_going_attempt(db, topic.id, user.id)
    if going_attempt is not None:
        raise bad_request('Cannot make new test until there is unfinished one.')

    return queries.create_attempt(db, topic, user.id)
