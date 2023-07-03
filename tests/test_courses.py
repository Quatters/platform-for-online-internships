from sqlalchemy.orm import Session
from backend.models import User, UserCompetence
from tests.base import login_as, test_admin, test_intern
from tests.helpers import (
    create_competence,
    create_course,
    create_post,
    create_subdivision,
    get_records_count,
)


def test_courses_crud(db: Session):
    client = login_as(test_admin)

    # create course
    response = client.post('/api/courses', json={
        'name': 'course_1',
        'description': 'course_1',
        'competencies': [],
        'posts': [],
    })
    data = response.json()
    assert response.status_code == 200, data
    course_1_id = data['id']

    # get course
    response = client.get(f'/api/courses/{course_1_id}')
    data_2 = response.json()
    assert response.status_code == 200
    assert data == data_2

    # add competencies to course
    competence = create_competence(db)

    response = client.patch(f'/api/courses/{course_1_id}', json={
        'competencies': [competence.id]
    })
    data = response.json()
    assert response.status_code == 200
    assert len(data['competencies']) == 1

    # create another course and get all courses
    courses_count = get_records_count(route='/api/courses/', client=client)
    create_course(db)
    response = client.get('/api/courses/')
    data = response.json()
    assert response.status_code == 200, data
    assert len(data['items']) == courses_count + 1

    # delete course
    courses_count = get_records_count(route='/api/courses/', client=client)
    response = client.delete(f'/api/courses/{course_1_id}')
    assert response.status_code == 204
    response = client.get('/api/courses/')
    data = response.json()
    assert response.status_code == 200, data
    assert len(data['items']) == courses_count - 1


def test_recommended_courses(db: Session):
    client = login_as(test_intern)
    intern = db.query(User).filter(User.email == test_intern.email).one()

    intern_competence = create_competence(db)
    other_competence = create_competence(db)

    subdivision = create_subdivision(db)

    intern_post = create_post(db, subdivision_id=subdivision.id)
    other_intern_post = create_post(db, subdivision_id=subdivision.id)
    other_post = create_post(db, subdivision_id=subdivision.id)

    intern.user_competencies = [UserCompetence(user_id=intern.id, competence_id=intern_competence.id)]
    intern.posts = [intern_post, other_intern_post]
    db.commit()

    first_suitable_course = create_course(
        db,
        posts=[intern_post, other_post],
        competencies=[intern_competence, other_competence],
        name='first'
    )
    second_suitable_course = create_course(
        db,
        posts=[other_intern_post],
        competencies=[intern_competence, other_competence],
        name='second'
    )
    # unsuitable by posts course
    create_course(
        db,
        posts=[other_post],
        competencies=[intern_competence, other_competence],
    )
    # unsuitable by competencies course
    create_course(
        db,
        posts=[intern_post, other_post],
        competencies=[intern_competence],
    )

    response = client.get('/api/courses/recommended')
    data = response.json()
    assert response.status_code == 200
    assert data['total'] == 2
    assert data['items'][0]['id'] == first_suitable_course.id
    assert data['items'][1]['id'] == second_suitable_course.id

    response = client.get(f'/api/courses/recommended?post_id={other_intern_post.id}')
    data = response.json()
    assert response.status_code == 200
    assert data['total'] == 1
    assert data['items'][0]['id'] == second_suitable_course.id
