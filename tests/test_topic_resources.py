from typing import Optional
from fastapi import Depends
import pytest
from uuid import uuid1
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from tests.base import login_as, test_admin
from backend.models import TopicResource, Topic, Course
from backend.database import get_db
from backend.constants import TopicResourceType
from tests import helpers


def test_topic_resource_model():
    db = next(get_db())

    course = helpers.create_course()
    topic = helpers.create_topic(course_id=course.id, db=db)

    resource_1 = helpers.create_topic_resource(topic_id=topic.id, db=db)

    # check cannot set self id as prev_resource_id
    with pytest.raises(IntegrityError):
        with db.begin_nested() as transaction:
            resource_1.prev_resource_id = resource_1.id
            transaction.commit()

    resource_2 = helpers.create_topic_resource(topic_id=topic.id, prev_resource_id=resource_1.id, db=db)

    # check cannot have more than one resources pointing on the same previous
    # resource
    resource_3 = helpers.create_topic_resource(topic_id=topic.id, prev_resource_id=resource_2.id, db=db)

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


def test_get_topic_resources_list():
    client = login_as(test_admin)

    course = helpers.create_course()
    topic = helpers.create_topic(course_id=course.id)

    response = client.get(f'/api/courses/{course.id}/topics/{topic.id}/resources/')
    assert response.status_code == 200
    data = response.json()
    assert data['items'] == []

    topic_2 = helpers.create_topic(course_id=course.id)

    db = next(get_db())

    helpers.create_topic_resource(topic_id=topic_2.id)
    resource_1 = helpers.create_topic_resource(topic_id=topic.id, db=db)
    resource_2 = helpers.create_topic_resource(topic_id=topic.id)
    resource_3 = helpers.create_topic_resource(topic_id=topic.id, prev_resource_id=resource_2.id)
    resource_1.prev_resource_id = resource_3.id
    db.commit()

    response = client.get(f'/api/courses/{course.id}/topics/{topic.id}/resources/')
    assert response.status_code == 200
    data = response.json()
    # check resource from other topic not here
    assert data['total'] == 3
    # check sorting
    assert data['items'][0]['id'] == resource_2.id
