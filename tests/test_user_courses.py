from backend.models import User, UserCourse
from tests.base import login_as, test_intern
from tests import helpers


def test_user_tests_crud(db):
    course = helpers.create_course(db)

    intern = db.query(User).filter(User.email == test_intern.email).one()
    client = login_as(test_intern)

    intern2 = helpers.create_user(db)

    # check empty list
    response = client.get(f'/api/user/{intern.id}/courses')
    data = response.json()
    assert response.status_code == 200, data
    assert data['total'] == 0

    # get invalid course
    response = client.get(f'/api/user/{intern.id}/courses/-1')
    data = response.json()
    assert response.status_code == 404, data

    # add invalid course
    response = client.post(f'/api/user/{intern.id}/courses', json={'course_id': -1})
    data = response.json()
    assert response.status_code == 404, data

    # add course
    response = client.post(f'/api/user/{intern.id}/courses', json={'course_id': course.id})
    data = response.json()
    assert response.status_code == 200, data
    assert data == {
        'id': data['id'],
        'user_id': intern.id,
        'course_id': course.id,
        'progress': 0.0,
        'admission_date': data['admission_date'],
    }

    # add course again
    response = client.post(f'/api/user/{intern.id}/courses', json={'course_id': course.id})
    data = response.json()
    assert response.status_code == 400, data
    assert data == {'detail': 'User is already registered for this course'}

    # get list courses
    response = client.get(f'/api/user/{intern.id}/courses')
    data = response.json()
    assert response.status_code == 200, data
    assert data['total'] == 1
    assert data['items'][0] == {
        'id': data['items'][0]['id'],
        'user_id': intern.id,
        'course_id': course.id,
        'course_name': course.name,
        'progress': 0.0,
        'admission_date': data['items'][0]['admission_date'],
        'pass_percent': course.pass_percent,
    }

    # search by course name
    response = client.get(f'/api/user/{intern.id}/courses?search=not_existing')
    data = response.json()
    assert response.status_code == 200, data
    assert data['total'] == 0
    assert data['items'] == []

    # get one course
    response = client.get(f'/api/user/{intern.id}/courses/{course.id}')
    data = response.json()
    assert response.status_code == 200, data
    assert data == {
        'id': data['id'],
        'user_id': intern.id,
        'course_id': course.id,
        'course_name': course.name,
        'progress': 0.0,
        'admission_date': data['admission_date'],
        'posts': [],
        'competencies': [],
        'course_description': course.description,
    }

    # delete invalid course
    response = client.delete(f'/api/user/{intern.id}/courses/-1')
    assert response.status_code == 404

    # delete course
    response = client.delete(f'/api/user/{intern.id}/courses/{course.id}')
    assert response.status_code == 204

    assert db.query(UserCourse).all() == []

    # get courses for another user
    response = client.get(f'/api/user/{intern2.id}/courses')
    data = response.json()
    assert response.status_code == 404
