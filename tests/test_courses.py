from tests.base import login_as, test_admin
from tests.helpers import create_competence, create_course, get_records_count


def test_courses_crud():
    client = login_as(test_admin)

    #create course
    response = client.post('/api/courses', json={
        'name': 'course_1',
        'description': 'course_1',
        'competencies': [],
    })
    data = response.json()
    assert response.status_code == 200, data
    course_1_id = data['id']


    #get course
    response = client.get(f'/api/courses/{course_1_id}')
    data_2 = response.json()
    assert response.status_code == 200
    assert data == data_2

    # add competencies to course
    competence = create_competence()

    response = client.patch(f'/api/courses/{course_1_id}', json={
        'competencies': [competence.id]
    })
    data = response.json()
    assert response.status_code == 200
    assert len(data['competencies']) == 1

    #create another course and get all courses
    courses_count = get_records_count(route='/api/courses/', client=client)
    create_course()
    response = client.get('/api/courses/')
    data = response.json()
    assert response.status_code == 200, data
    assert len(data['items']) == courses_count + 1


    #delete course
    courses_count = get_records_count(route='/api/courses/', client=client)
    response = client.delete(f'/api/courses/{course_1_id}')
    assert response.status_code == 204
    response = client.get('/api/courses/')
    data = response.json()
    assert response.status_code == 200, data
    assert len(data['items']) == courses_count - 1
