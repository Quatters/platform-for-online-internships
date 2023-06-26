import pytest
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from tests.base import login_as, test_admin
from backend.models import TopicResource
from tests import helpers


def test_topic_resource_model(db: Session):
    course = helpers.create_course(db)
    topic = helpers.create_topic(db, course_id=course.id)

    resource_1 = helpers.create_topic_resource(db, topic_id=topic.id)

    # check cannot set self id as prev_resource_id
    with pytest.raises(IntegrityError):
        resource_1.prev_resource_id = resource_1.id
        db.commit()
    db.rollback()

    resource_2 = helpers.create_topic_resource(db, topic_id=topic.id, prev_resource_id=resource_1.id)

    # check cannot have more than one resources pointing on the same previous
    # resource
    resource_3 = helpers.create_topic_resource(db, topic_id=topic.id, prev_resource_id=resource_2.id)

    with pytest.raises(IntegrityError):
        resource_3.prev_resource_id = resource_1.id
        db.commit()
    db.rollback()

    resource_3.prev_resource_id = resource_2.id
    db.commit()
    db.refresh(resource_3)

    assert resource_1.prev_resource is None
    assert resource_1.next_resource.id == resource_2.id

    assert resource_2.prev_resource.id == resource_1.id
    assert resource_2.next_resource.id == resource_3.id

    assert resource_3.prev_resource.id == resource_2.id
    assert resource_3.next_resource is None


def test_topic_resources_crud(db: Session):
    client = login_as(test_admin)

    course = helpers.create_course(db)
    topic = helpers.create_topic(db, course_id=course.id)

    # test list page
    response = client.get(f'/api/courses/{course.id}/topics/{topic.id}/resources/')
    assert response.status_code == 200
    data = response.json()
    assert data['items'] == []

    topic_2 = helpers.create_topic(db, course_id=course.id)

    helpers.create_topic_resource(db, topic_id=topic_2.id)
    resource_1 = helpers.create_topic_resource(db, topic_id=topic.id)
    resource_2 = helpers.create_topic_resource(db, topic_id=topic.id)
    resource_3 = helpers.create_topic_resource(db, topic_id=topic.id, prev_resource_id=resource_2.id)
    resource_1.prev_resource_id = resource_3.id
    db.commit()

    response = client.get(f'/api/courses/{course.id}/topics/{topic.id}/resources/')
    assert response.status_code == 200
    data = response.json()
    # check resource from other topic not here
    assert data['total'] == 3
    # check sorting
    assert data['items'][0]['id'] == resource_2.id

    # test detail page
    response = client.get(f'/api/courses/{course.id}/topics/{topic.id}/resources/{resource_3.id}')
    assert response.status_code == 200
    data = response.json()
    assert data == {
        'id': resource_3.id,
        'name': resource_3.name,
        'value': resource_3.value,
        'type': str(resource_3.type),
        'next_resource': {
            'id': resource_3.next_resource.id,
            'name': resource_3.next_resource.name,
        },
        'prev_resource': {
            'id': resource_3.prev_resource.id,
            'name': resource_3.prev_resource.name,
        },
    }

    # test create resource with invalid prev_resource_id
    response = client.post(
        f'/api/courses/{course.id}/topics/{topic.id}/resources',
        json={
            'name': 'new_first',
            'value': 'value',
            'type': 'text',
            'prev_resource_id': -1,
        },
    )
    data = response.json()
    assert response.status_code == 400, data
    assert data['detail'] == 'Instance with id -1 does not exist.'

    # test create first resource if first already exists
    response = client.post(
        f'/api/courses/{course.id}/topics/{topic.id}/resources',
        json={
            'name': 'new_first',
            'value': 'value',
            'type': 'text',
            'prev_resource_id': None,
        },
    )
    data = response.json()
    assert response.status_code == 200, data
    db.refresh(resource_2)
    resource_4: TopicResource | None = db.query(TopicResource).get(data['id'])
    assert resource_4 is not None
    assert resource_4.prev_resource is None
    assert resource_4.next_resource.id == resource_2.id
    assert resource_2.prev_resource_id == resource_4.id

    # test create resource at the middle
    response = client.post(
        f'/api/courses/{course.id}/topics/{topic.id}/resources',
        json={
            'name': 'new_first',
            'value': 'value',
            'type': 'text',
            'prev_resource_id': resource_4.id,
        },
    )
    data = response.json()
    assert response.status_code == 200, data
    db.refresh(resource_4)
    db.refresh(resource_2)
    resource_5 = db.query(TopicResource).get(data['id'])
    assert resource_5 is not None
    assert resource_4.prev_resource is None
    assert resource_4.next_resource.id == resource_5.id
    assert resource_2.prev_resource_id == resource_5.id
    assert resource_5.prev_resource.id == resource_4.id
    assert resource_5.next_resource.id == resource_2.id

    # test update resource without updating prev_resource_id
    response = client.patch(
        f'/api/courses/{course.id}/topics/{topic.id}/resources/{resource_5.id}',
        json={
            'name': 'second',
        },
    )
    data = response.json()
    assert response.status_code == 200, data
    db.refresh(resource_4)
    db.refresh(resource_2)
    db.refresh(resource_5)
    assert resource_4.prev_resource is None
    assert resource_4.next_resource.id == resource_5.id
    assert resource_2.prev_resource_id == resource_5.id
    assert resource_5.prev_resource.id == resource_4.id
    assert resource_5.next_resource.id == resource_2.id

    # test update resource (set first)
    response = client.patch(
        f'/api/courses/{course.id}/topics/{topic.id}/resources/{resource_5.id}',
        json={
            'prev_resource_id': None,
        },
    )
    data = response.json()
    assert response.status_code == 200, data
    db.refresh(resource_4)
    db.refresh(resource_2)
    db.refresh(resource_5)
    assert resource_5.prev_resource_id is None
    assert resource_5.next_resource.id == resource_4.id
    assert resource_4.prev_resource_id == resource_5.id

    # test update resource (set to middle)
    response = client.patch(
        f'/api/courses/{course.id}/topics/{topic.id}/resources/{resource_5.id}',
        json={
            'prev_resource_id': resource_4.id,
        },
    )
    data = response.json()
    assert response.status_code == 200, data
    db.refresh(resource_4)
    db.refresh(resource_2)
    db.refresh(resource_5)
    assert resource_5.prev_resource_id == resource_4.id
    assert resource_5.next_resource.id == resource_2.id
    assert resource_4.prev_resource_id is None
    assert resource_4.next_resource.id == resource_5.id

    # test update resource (set last)
    current_next_resource = resource_5.next_resource
    current_prev_resource = resource_5.prev_resource
    response = client.patch(
        f'/api/courses/{course.id}/topics/{topic.id}/resources/{resource_5.id}',
        json={
            'prev_resource_id': resource_1.id,
        },
    )
    data = response.json()
    assert response.status_code == 200, data
    db.refresh(resource_1)
    db.refresh(resource_5)
    db.refresh(resource_2)
    assert resource_5.next_resource is None
    assert resource_5.prev_resource.id == resource_1.id
    assert current_next_resource.prev_resource_id == current_prev_resource.id

    # get result list
    response = client.get(f'/api/courses/{course.id}/topics/{topic.id}/resources/')
    data = response.json()
    assert response.status_code == 200, data
    assert data['total'] == 5
    assert [item['id'] for item in data['items']] == [
        resource_4.id,
        resource_2.id,
        resource_3.id,
        resource_1.id,
        resource_5.id,
    ]

    # delete resource_3 (middle)
    response = client.delete(f'/api/courses/{course.id}/topics/{topic.id}/resources/{resource_3.id}')
    assert response.status_code == 204
    # get result list
    response = client.get(f'/api/courses/{course.id}/topics/{topic.id}/resources/')
    data = response.json()
    assert response.status_code == 200, data
    assert data['total'] == 4
    assert [item['id'] for item in data['items']] == [
        resource_4.id,
        resource_2.id,
        resource_1.id,
        resource_5.id,
    ]

    # delete resource_4 (first)
    response = client.delete(f'/api/courses/{course.id}/topics/{topic.id}/resources/{resource_4.id}')
    assert response.status_code == 204
    # get result list
    response = client.get(f'/api/courses/{course.id}/topics/{topic.id}/resources/')
    data = response.json()
    assert response.status_code == 200, data
    assert data['total'] == 3
    assert [item['id'] for item in data['items']] == [
        resource_2.id,
        resource_1.id,
        resource_5.id,
    ]

    # delete resource_5 (last)
    response = client.delete(f'/api/courses/{course.id}/topics/{topic.id}/resources/{resource_5.id}')
    assert response.status_code == 204
    # get result list
    response = client.get(f'/api/courses/{course.id}/topics/{topic.id}/resources/')
    data = response.json()
    assert response.status_code == 200, data
    assert data['total'] == 2
    assert [item['id'] for item in data['items']] == [
        resource_2.id,
        resource_1.id,
    ]
