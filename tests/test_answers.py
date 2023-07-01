from backend.constants import TaskType
from backend.models import Answer
from tests.base import login_as, test_admin
from tests import helpers


def test_answers_crud(db):
    course = helpers.create_course(db)
    topic = helpers.create_topic(db, course_id=course.id)
    task_single = helpers.create_task(db, topic_id=topic.id, task_type=TaskType.single)

    admin_client = login_as(test_admin)

    # create correct answer
    response = admin_client.post(f'/api/courses/{course.id}/topics/{topic.id}/tasks/{task_single.id}/answers', json={
        'value': 'value_1',
        'is_correct': True,
    })
    data = response.json()
    assert response.status_code == 200, data
    assert data == {
        'id': data['id'],
        'value': 'value_1',
        'is_correct': True,
    }

    # create another correct answer
    response = admin_client.post(f'/api/courses/{course.id}/topics/{topic.id}/tasks/{task_single.id}/answers', json={
        'value': 'value_2',
        'is_correct': True,
    })
    data = response.json()
    assert response.status_code == 200, data
    assert data == {
        'id': data['id'],
        'value': 'value_2',
        'is_correct': True,
    }

    # get list
    response = admin_client.get(f'/api/courses/{course.id}/topics/{topic.id}/tasks/{task_single.id}/answers')
    data = response.json()
    assert response.status_code == 200, data
    assert data['total'] == 2
    assert data['items'] == [
        {'id': data['items'][0]['id'], 'value': 'value_1', 'is_correct': False},
        {'id': data['items'][1]['id'], 'value': 'value_2', 'is_correct': True},
    ]

    answer_1_id = data['items'][0]['id']
    answer_2_id = data['items'][1]['id']

    # get one answer
    response = admin_client.get(
        f'/api/courses/{course.id}/topics/{topic.id}/tasks/{task_single.id}/answers/{answer_1_id}',
    )
    data = response.json()
    assert response.status_code == 200, data
    assert data == {'id': answer_1_id, 'value': 'value_1', 'is_correct': False}

    # get non-existing answer
    response = admin_client.get(
        f'/api/courses/{course.id}/topics/{topic.id}/tasks/{task_single.id}/answers/-1',
    )
    assert response.status_code == 404

    # patch answer
    response = admin_client.patch(
        f'/api/courses/{course.id}/topics/{topic.id}/tasks/{task_single.id}/answers/{answer_1_id}',
        json={'value': 'new_value_1', 'is_correct': True}
    )
    data = response.json()
    assert response.status_code == 200, data
    assert data['value'] == 'new_value_1'
    assert data['is_correct'] is True
    assert db.get(Answer, answer_2_id).is_correct is False

    # delete answer
    response = admin_client.delete(
        f'/api/courses/{course.id}/topics/{topic.id}/tasks/{task_single.id}/answers/{answer_1_id}',
    )
    assert response.status_code == 204
    assert db.query(Answer).filter(Answer.id == answer_1_id).all() == []

    task_text = helpers.create_task(db, task_type=TaskType.text, topic_id=topic.id)

    # try to get answer for text task
    response = admin_client.get(
        f'/api/courses/{course.id}/topics/{topic.id}/tasks/{task_text.id}/answers',
    )
    data = response.json()
    assert response.status_code == 400, data
    assert data == {'detail': 'Unsuitable task type'}
