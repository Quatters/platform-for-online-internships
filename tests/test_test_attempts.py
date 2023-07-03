from sqlalchemy.orm import Session
from backend.constants import TaskType
from backend.models import TestAttempt, User, UserCompetence
from tests.base import login_as, test_intern, test_teacher
from tests import helpers


def test_tests(db: Session):
    course = helpers.create_course(db, pass_percent=75)
    topic = helpers.create_topic(db, course_id=course.id)
    competence_which_user_has = helpers.create_competence(db, courses=[course])
    competence_to_achieve = helpers.create_competence(db, courses=[course])

    task_1 = helpers.create_task(db, topic_id=topic.id, task_type=TaskType.single)
    task_2 = helpers.create_task(db, topic_id=topic.id, task_type=TaskType.multiple, prev_task_id=task_1.id)
    task_3 = helpers.create_task(db, topic_id=topic.id, task_type=TaskType.text, prev_task_id=task_2.id)

    answer_1_1_correct = helpers.create_answer(db, task_id=task_1.id, is_correct=True)
    answer_1_2 = helpers.create_answer(db, task_id=task_1.id)
    answer_1_3 = helpers.create_answer(db, task_id=task_1.id)

    answer_2_1_correct = helpers.create_answer(db, task_id=task_2.id, is_correct=True)
    answer_2_2 = helpers.create_answer(db, task_id=task_2.id)
    answer_2_3_correct = helpers.create_answer(db, task_id=task_2.id, is_correct=True)

    intern = db.query(User).filter(User.email == test_intern.email).one()
    teacher = db.query(User).filter(User.email == test_teacher.email).one()
    intern.teacher = teacher
    intern.user_competencies = [UserCompetence(user_id=intern.id, competence_id=competence_which_user_has.id)]
    db.commit()

    intern = db.query(User).filter(User.email == test_intern.email).one()
    teacher = db.query(User).filter(User.email == test_teacher.email).one()
    intern.teacher = teacher
    db.commit()

    intern_client = login_as(test_intern)
    teacher_client = login_as(test_teacher)

    # check no attempts for now
    response = intern_client.get('/api/tests')
    data = response.json()
    assert response.status_code == 200, data
    assert data['total'] == 0

    # try to start test without user course
    response = intern_client.post(f'/api/courses/{course.id}/topics/{topic.id}/start_test')
    data = response.json()
    assert response.status_code == 400, data
    assert data == {'detail': 'You cannot start test on a course you are not enrolled in.'}

    user_course = helpers.create_user_course(db, user_id=intern.id, course_id=course.id)

    # start test (1)
    response = intern_client.post(f'/api/courses/{course.id}/topics/{topic.id}/start_test')
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
                        'id': answer_1_1_correct.id,
                        'value': answer_1_1_correct.value,
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
                        'id': answer_2_1_correct.id,
                        'value': answer_2_1_correct.value,
                    },
                    {
                        'id': answer_2_2.id,
                        'value': answer_2_2.value,
                    },
                    {
                        'id': answer_2_3_correct.id,
                        'value': answer_2_3_correct.value,
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
    response = intern_client.post(f'/api/courses/{course.id}/topics/{topic.id}/start_test')
    data = response.json()
    assert response.status_code == 400, data
    assert data['detail'] == 'Cannot start new test until there is unfinished one.'

    # get going test
    response = intern_client.get('/api/tests/going')
    data = response.json()
    assert response.status_code == 200, data
    assert data == test_with_tasks_data_to_check

    # check for now user_course.progress is 0
    db.refresh(user_course)
    assert user_course.progress == 0
    # check that intern has only his competence
    db.refresh(intern)
    assert len(intern.competencies) == 1
    assert intern.user_competencies[0].competence_id == competence_which_user_has.id

    # finish test
    user_answers = [
        {'task_id': task_1.id, 'answer': answer_1_1_correct.id},
        {'task_id': task_2.id, 'answer': [answer_2_1_correct.id, answer_2_2.id]},
        {'task_id': task_3.id, 'answer': 'some text for teacher'},
    ]

    response = intern_client.post(f'/api/tests/{test_id}/finish', json=user_answers)
    data = response.json()
    assert response.status_code == 200, data
    assert data == {'detail': 'Test submitted.'}

    # try to get reviews as intern
    response = intern_client.get('/api/reviews')
    assert response.status_code == 403

    # check teacher's reviews
    response = teacher_client.get('/api/reviews')
    data = response.json()
    assert response.status_code == 200, data
    assert data['total'] == 1
    review_id = data['items'][0]['id']
    assert data['items'][0] == {
        'id': review_id,
        'task_name': task_3.name,
        'status': 'unchecked',
    }

    # check one teacher's review
    response = teacher_client.get(f'/api/reviews/{review_id}')
    data = response.json()
    assert response.status_code == 200, data
    assert data == {
        'id': review_id,
        'task_name': task_3.name,
        'task_description': task_3.description,
        'max_score': 5,
        'score': 0,
        'value': 'some text for teacher',
        'review': None,
        'status': 'unchecked',
    }

    # get test list
    response = intern_client.get('/api/tests')
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
    response = intern_client.get(f'/api/tests/{test_id}')
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
        'user_answers': [
            {
                'id': data['user_answers'][0]['id'],
                'task_name': task_1.name,
                'task_description': task_1.description,
                'task_type': task_1.task_type.value,
                'value': answer_1_1_correct.value,
                'score': 1,
                'max_score': 1,
                'status': 'checked',
                'review': None,
            },
            {
                'id': data['user_answers'][1]['id'],
                'task_name': task_2.name,
                'task_description': task_2.description,
                'task_type': task_2.task_type.value,
                'value': [answer_2_1_correct.value, answer_2_2.value],
                'score': 1,
                'max_score': 2,
                'status': 'checked',
                'review': None,
            },
            {
                'id': review_id,
                'task_name': task_3.name,
                'task_description': task_3.description,
                'task_type': task_3.task_type.value,
                'value': 'some text for teacher',
                'score': 0,
                'max_score': 5,
                'status': 'unchecked',
                'review': None,
            },
        ],
    }
    # check that user_course.progress updated
    db.refresh(user_course)
    assert user_course.progress == 25.0  # = (1 + 1 + 0) / (1 + 2 + 5) * 100
    # check that intern has only his competence
    db.refresh(intern)
    assert len(intern.competencies) == 1
    assert intern.user_competencies[0].competence_id == competence_which_user_has.id

    # finish review as teacher
    response = teacher_client.put(f'/api/reviews/{review_id}', json={
        'score': 4,
        'review': 'good job',
    })
    data = response.json()
    assert response.status_code == 200, data

    # invalid review
    response = teacher_client.put('/api/reviews/-1', json={
        'score': 4,
        'review': 'good job',
    })
    assert response.status_code == 404

    # get same test, check that last answer is reviewed
    response = intern_client.get(f'/api/tests/{test_id}')
    data = response.json()
    assert response.status_code == 200, data
    assert data['user_answers'][-1] == {
        'id': review_id,
        'task_name': task_3.name,
        'task_description': task_3.description,
        'task_type': task_3.task_type.value,
        'value': 'some text for teacher',
        'score': 4,
        'max_score': 5,
        'status': 'checked',
        'review': 'good job',
    }
    assert data['score'] == 6
    assert data['status'] == 'checked'
    # check that user_course.progress updated
    db.refresh(user_course)
    assert user_course.progress == 75.0  # = (1 + 1 + 4) / (1 + 2 + 5) * 100
    # and intern got competence
    db.refresh(intern)
    assert len(intern.competencies) == 2
    assert intern.user_competencies[0].competence_id == competence_which_user_has.id
    assert intern.user_competencies[1].competence_id == competence_to_achieve.id

    # try to get not existing test
    response = intern_client.get('/api/tests/-1')
    data = response.json()
    assert response.status_code == 404, data

    # check submitting test (2) with timeout
    response = intern_client.post(f'/api/courses/{course.id}/topics/{topic.id}/start_test')
    data = response.json()
    assert response.status_code == 200, data
    test_id: int = data['id']
    test = db.get(TestAttempt, test_id)
    test.time_to_pass = 0
    db.commit()
    # check that user_course.progress is the same
    db.refresh(user_course)
    assert user_course.progress == 75.0

    # try to submit
    response = intern_client.post(f'/api/tests/{test_id}/finish', json=user_answers)
    data = response.json()
    assert response.status_code == 200, data
    assert data == {'detail': 'Test submitted.'}

    # get test
    response = intern_client.get(f'/api/tests/{test_id}')
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
        'user_answers': [],
    }

    # start test (3)
    response = intern_client.post(f'/api/courses/{course.id}/topics/{topic.id}/start_test')
    data = response.json()
    assert response.status_code == 200, data
    test_id = data['id']

    # finish test sending only system-checking answers
    response = intern_client.post(f'/api/tests/{test_id}/finish', json=[
        {'task_id': task_1.id, 'answer': answer_1_1_correct.id},
        {'task_id': task_2.id, 'answer': [answer_2_1_correct.id, answer_2_3_correct.id]},
    ])
    data = response.json()
    assert response.status_code == 200, data
    assert data == {'detail': 'Test submitted.'}
    # check that user_course.progress is the same
    db.refresh(user_course)
    assert user_course.progress == 75.0

    # get test
    response = intern_client.get(f'/api/tests/{test_id}')
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
        'user_answers': [
            {
                'id': data['user_answers'][0]['id'],
                'task_name': task_1.name,
                'task_description': task_1.description,
                'task_type': task_1.task_type.value,
                'value': answer_1_1_correct.value,
                'score': 1,
                'max_score': 1,
                'status': 'checked',
                'review': None,
            },
            {
                'id': data['user_answers'][1]['id'],
                'task_name': task_2.name,
                'task_description': task_2.description,
                'task_type': task_2.task_type.value,
                'value': [answer_2_1_correct.value, answer_2_3_correct.value],
                'score': 2,
                'max_score': 2,
                'status': 'checked',
                'review': None,
            },
        ]
    }

    # start test (4, must not be allowed)
    response = intern_client.post(f'/api/courses/{course.id}/topics/{topic.id}/start_test')
    data = response.json()
    assert response.status_code == 400, data
    assert data['detail'] == 'You have run out of attempts for this topic.'

    # check that for intern 'attempts_amount' is available attempts
    response = intern_client.get(f'/api/courses/{course.id}/topics/{topic.id}')
    data = response.json()
    assert response.status_code == 200, data
    assert data['attempts_amount'] == 0

    # remove user_course
    response = intern_client.delete(f'/api/user/{intern.id}/courses/{course.id}')
    assert response.status_code == 204

    # create another user_course
    response = intern_client.post(f'/api/user/{intern.id}/courses', json={
        'course_id': course.id,
    })
    assert response.status_code == 200

    # check that attempts reset
    response = intern_client.get(f'/api/courses/{course.id}/topics/{topic.id}')
    data = response.json()
    assert response.status_code == 200, data
    assert data['attempts_amount'] == 3

    response = intern_client.post(f'/api/courses/{course.id}/topics/{topic.id}/start_test')
    data = response.json()
    assert response.status_code == 200, data
