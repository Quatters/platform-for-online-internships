from sqlalchemy.orm import Session
from tests.base import login_as, test_admin
from tests.helpers import create_competence, create_course, get_records_count


def test_competencies_crud(db: Session):
    client = login_as(test_admin)

    # create competence
    response = client.post('/api/competencies', json={
        'name': 'competence_1',
        'courses': [],
        'posts': [],
    })
    data = response.json()
    assert response.status_code == 200, data
    competence_1_id = data['id']

    # get competence
    response = client.get(f'/api/competencies/{competence_1_id}')
    data_2 = response.json()
    assert response.status_code == 200
    assert data == data_2

    # get invalid competence
    response = client.get('/api/competencies/-1')
    assert response.status_code == 404

    # add courses to competence
    course = create_course(db)
    response = client.patch(f'/api/competencies/{competence_1_id}', json={
        'courses': [course.id]
    })
    data = response.json()
    assert response.status_code == 200
    assert len(data['courses']) == 1

    # create another competence and get all competencies
    competence_count = get_records_count(route='/api/competencies/', client=client)
    create_competence(db)
    response = client.get('/api/competencies/')
    data = response.json()
    assert response.status_code == 200, data
    assert len(data['items']) == competence_count + 1

    # delete competence
    competence_count = get_records_count(route='/api/competencies/', client=client)
    response = client.delete(f'/api/competencies/{competence_1_id}')
    assert response.status_code == 204
    response = client.get('/api/competencies/')
    data = response.json()
    assert response.status_code == 200, data
    assert len(data['items']) == competence_count - 1
