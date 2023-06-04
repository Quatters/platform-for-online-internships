from tests import helpers
from tests.base import login_as, test_admin


def test_topics_crud():
    client = login_as(test_admin)

    course = helpers.create_course()

    response = client.post(f'/api/courses/{course.id}/topics', json={
        'name': 'topic_1',
        'description': 'topic_1',
    })
    data = response.json()
    assert response.status_code == 200, data
    topic_1_id = data['id']

    response = client.post(f'/api/courses/{course.id}/topics', json={
        'name': 'topic_2',
        'description': 'topic_2',
        'prev_topic_id': topic_1_id,
    })
    data = response.json()
    assert response.status_code == 200, data
    topic_2_id = data['id']

    response = client.post(f'/api/courses/{course.id}/topics', json={
        'name': 'topic_3',
        'description': 'topic_3',
        'prev_topic_id': None,
    })
    data = response.json()
    assert response.status_code == 200, data
    topic_3_id = data['id']

    # check that now first is topic_3
    response = client.get(f'/api/courses/{course.id}/topics')
    data = response.json()
    assert response.status_code == 200
    assert data['total'] == 3
    assert [item['id'] for item in data['items']] == [
        topic_3_id,
        topic_1_id,
        topic_2_id,
    ]

    # update topic_3, make it last
    response = client.patch(f'/api/courses/{course.id}/topics/{topic_3_id}', json={
        'prev_topic_id': topic_2_id,
    })
    data = response.json()
    assert response.status_code == 200, data
    response = client.get(f'/api/courses/{course.id}/topics')
    data = response.json()
    assert response.status_code == 200
    assert data['total'] == 3
    assert [item['id'] for item in data['items']] == [
        topic_1_id,
        topic_2_id,
        topic_3_id,
    ]

    # delete at the middle
    response = client.delete(f'/api/courses/{course.id}/topics/{topic_2_id}')
    assert response.status_code == 204
    response = client.get(f'/api/courses/{course.id}/topics')
    data = response.json()
    assert response.status_code == 200
    assert data['total'] == 2
    assert [item['id'] for item in data['items']] == [
        topic_1_id,
        topic_3_id,
    ]

    # delete first
    response = client.delete(f'/api/courses/{course.id}/topics/{topic_1_id}')
    assert response.status_code == 204
    response = client.get(f'/api/courses/{course.id}/topics')
    data = response.json()
    assert response.status_code == 200
    assert data['total'] == 1
    assert [item['id'] for item in data['items']] == [
        topic_3_id,
    ]

    # delete last
    response = client.delete(f'/api/courses/{course.id}/topics/{topic_3_id}')
    assert response.status_code == 204
    response = client.get(f'/api/courses/{course.id}/topics')
    data = response.json()
    assert response.status_code == 200
    assert data['total'] == 0
