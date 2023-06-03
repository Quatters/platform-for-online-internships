import pytest
from sqlalchemy.exc import IntegrityError
from tests.base import login_as, test_admin
from backend.models import TopicResource, Topic, Course
from backend.database import get_db
from backend.constants import TopicResourceType

def test_topic_resource_model():
    db = next(get_db())

    course = Course(name='course')
    db.add(course)
    db.commit()
    db.refresh(course)

    topic = Topic(name='topic', description='', course_id=course.id)
    db.add(topic)
    db.commit()
    db.refresh(topic)

    resource_1 = TopicResource(
        type=TopicResourceType.text,
        value='text',
        topic_id=topic.id,
    )
    db.add(resource_1)
    db.commit()
    db.refresh(resource_1)

    # check cannot set self id as prev_resource_id
    with pytest.raises(IntegrityError):
        with db.begin_nested() as transaction:
            resource_1.prev_resource_id = resource_1.id
            transaction.commit()

    resource_2 = TopicResource(
        type=TopicResourceType.text,
        value='text',
        topic_id=topic.id,
        prev_resource_id=resource_1.id,
    )
    db.add(resource_2)
    db.commit()
    db.refresh(resource_2)

    # check cannot have more than one resources pointing on the same previous
    # resource
    resource_3 = TopicResource(
        type=TopicResourceType.text,
        value='text',
        topic_id=topic.id,
        prev_resource_id=resource_2.id,
    )
    db.add(resource_3)
    db.commit()
    db.refresh(resource_3)

    with pytest.raises(IntegrityError):
        with db.begin_nested() as transaction:
            resource_3.prev_resource_id = resource_1.id
            transaction.commit()

    resource_3.prev_resource_id = resource_2.id
    db.commit()
    db.refresh(resource_3)

    assert resource_1.prev_resource is None
    assert resource_1.next_resource.id == resource_2.id

    assert resource_2.prev_resource.id == resource_1.id
    assert resource_2.next_resource.id == resource_3.id

    assert resource_3.prev_resource.id == resource_2.id
    assert resource_3.next_resource is None
