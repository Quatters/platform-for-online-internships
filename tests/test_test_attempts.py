from backend.constants import TaskType
from backend.database import get_db
from backend.models.test_attempts import TestAttempt
from tests.base import login_as, test_intern
from tests import helpers


def test_tests():
    db = next(get_db())

    course = helpers.create_course()
    topic = helpers.create_topic(course_id=course.id)

    task_1 = helpers.create_task(topic_id=topic.id, task_type=TaskType.single)
    task_2 = helpers.create_task(topic_id=topic.id, task_type=TaskType.multiple, prev_task_id=task_1.id)
    task_3 = helpers.create_task(topic_id=topic.id, task_type=TaskType.text, prev_task_id=task_2.id)

    answer_1_1 = helpers.create_answer(task_id=task_1.id, is_correct=True)
    answer_1_2 = helpers.create_answer(task_id=task_1.id)
    answer_1_3 = helpers.create_answer(task_id=task_1.id)

    answer_2_1 = helpers.create_answer(task_id=task_2.id, is_correct=True)
    answer_2_2 = helpers.create_answer(task_id=task_2.id)
    answer_2_3 = helpers.create_answer(task_id=task_2.id, is_correct=True)

    client = login_as(test_intern)

    # check no attempts for now
    response = client.get('/api/tests')
    data = response.json()
    assert response.status_code == 200, data
    assert data['total'] == 0

    # start test
    response = client.post(f'/api/courses/{course.id}/topics/{topic.id}/start_test')
    data = response.json()
    assert response.status_code == 200, data
    test_id = data['id']

    test_with_tasks_data_to_check = {
        'id': test_id,
        'started_at': data['started_at'],
        'time_to_pass': (
            TaskType.single.time_to_pass
            + TaskType.multiple.time_to_pass
            + TaskType.text.time_to_pass
        ),
        'topic': {
            'id': topic.id,
            'course_id': course.id,
            'name': topic.name,
        },
        'tasks': [
            {
                'id': task_1.id,
                'name': task_1.name,
                'description': task_1.description,
                'task_type': 'single',
                'possible_answers': [
                    {
                        'id': answer_1_1.id,
                        'value': answer_1_1.value,
                    },
                    {
                        'id': answer_1_2.id,
                        'value': answer_1_2.value,
                    },
                    {
                        'id': answer_1_3.id,
                        'value': answer_1_3.value,
                    },
                ],
            },
            {
                'id': task_2.id,
                'name': task_2.name,
                'description': task_2.description,
                'task_type': 'multiple',
                'possible_answers': [
                    {
                        'id': answer_2_1.id,
                        'value': answer_2_1.value,
                    },
                    {
                        'id': answer_2_2.id,
                        'value': answer_2_2.value,
                    },
                    {
                        'id': answer_2_3.id,
                        'value': answer_2_3.value,
                    },
                ],
            },
            {
                'id': task_3.id,
                'name': task_3.name,
                'description': task_3.description,
                'task_type': 'text',
                'possible_answers': None,
            },
        ]
    }

    assert data == test_with_tasks_data_to_check

    # check can't start new test
    response = client.post(f'/api/courses/{course.id}/topics/{topic.id}/start_test')
    data = response.json()
    assert response.status_code == 400, data
    assert data['detail'] == 'Cannot start new test until there is unfinished one.'

    # get going test
    response = client.get('/api/tests/going')
    data = response.json()
    assert response.status_code == 200, data
    assert data == test_with_tasks_data_to_check

    # finish test
    user_answers = [
        {'task_id': task_1.id, 'answer': answer_1_1.id},
        {'task_id': task_2.id, 'answer': [answer_2_1.id, answer_2_2.id]},
        {'task_id': task_3.id, 'answer': 'some text for teacher'},
    ]

    response = client.post(f'/api/tests/{test_id}/finish', json=user_answers)
    data = response.json()
    assert response.status_code == 200, data
    assert data == {'detail': 'Test submitted.'}

    # get test list
    response = client.get('/api/tests')
    data = response.json()
    assert response.status_code == 200, data
    assert data['total'] == 1
    assert data['items'] == [{
        'id': test_id,
        'status': 'partially_checked',
        'course': {
            'id': course.id,
            'name': course.name,
        },
        'topic': {
            'id': topic.id,
            'course_id': course.id,
            'name': topic.name,
        },
    }]

    # get one test
    response = client.get(f'/api/tests/{test_id}')
    data = response.json()
    assert response.status_code == 200, data
    assert data == {
        'id': test_id,
        'status': 'partially_checked',
        'course': {
            'id': course.id,
            'name': course.name,
        },
        'topic': {
            'id': topic.id,
            'course_id': course.id,
            'name': topic.name,
        },
        'max_score': 8,
        'score': 2,
        'started_at': data['started_at'],
        'finished_at': data['finished_at'],
    }

    # try to get not existing test
    response = client.get('/api/tests/-1')
    data = response.json()
    assert response.status_code == 404, data

    # check submitting test with timeout
    response = client.post(f'/api/courses/{course.id}/topics/{topic.id}/start_test')
    data = response.json()
    assert response.status_code == 200, data
    test_id: int = data['id']
    test = db.query(TestAttempt).get(test_id)
    test.time_to_pass = 0
    db.commit()

    # try to submit
    response = client.post(f'/api/tests/{test_id}/finish', json=user_answers)
    data = response.json()
    assert response.status_code == 200, data
    assert data == {'detail': 'Test submitted.'}

    # get test
    response = client.get(f'/api/tests/{test_id}')
    data = response.json()
    assert response.status_code == 200, data
    assert data == {
        'id': test_id,
        'status': 'timeout_failure',
        'course': {
            'id': course.id,
            'name': course.name,
        },
        'topic': {
            'id': topic.id,
            'course_id': course.id,
            'name': topic.name,
        },
        'max_score': 8,
        'score': 0,
        'started_at': data['started_at'],
        'finished_at': data['finished_at'],
    }

    # start test
    response = client.post(f'/api/courses/{course.id}/topics/{topic.id}/start_test')
    data = response.json()
    assert response.status_code == 200, data
    test_id = data['id']

    # finish test sending only system-checking answers
    response = client.post(f'/api/tests/{test_id}/finish', json=[
        {'task_id': task_1.id, 'answer': answer_1_1.id},
        {'task_id': task_2.id, 'answer': [answer_2_1.id, answer_2_3.id]},
    ])
    data = response.json()
    assert response.status_code == 200, data
    assert data == {'detail': 'Test submitted.'}

    # get test
    response = client.get(f'/api/tests/{test_id}')
    data = response.json()
    assert response.status_code == 200, data
    assert data == {
        'id': test_id,
        'status': 'checked',
        'course': {
            'id': course.id,
            'name': course.name,
        },
        'topic': {
            'id': topic.id,
            'course_id': course.id,
            'name': topic.name,
        },
        'max_score': 8,
        'score': 3,
        'started_at': data['started_at'],
        'finished_at': data['finished_at'],
    }
