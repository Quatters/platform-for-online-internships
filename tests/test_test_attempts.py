from backend.constants import TaskType
from tests.base import login_as, test_admin, test_intern
from tests import helpers


def test_make_test_attempt():
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

    response = client.post(f'/api/courses/{course.id}/topics/{topic.id}/make_test')
    data = response.json()
    assert response.status_code == 200, data
