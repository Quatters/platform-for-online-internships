from backend.constants import TaskType
from tests.base import login_as, test_admin, test_intern
from tests import helpers


def test_tests():
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

    response = client.post(f'/api/courses/{course.id}/topics/{topic.id}/start_test')
    data = response.json()
    assert response.status_code == 200, data
    assert data == {
        'id': data['id'],
        'started_at': data['started_at'],
        'time_to_pass': (
            TaskType.single.time_to_pass
            + TaskType.multiple.time_to_pass
            + TaskType.text.time_to_pass
        ),
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

    # check can't start new test
    response = client.post(f'/api/courses/{course.id}/topics/{topic.id}/start_test')
    data = response.json()
    assert response.status_code == 400, data
    assert data['detail'] == 'Cannot start new test until there is unfinished one.'
