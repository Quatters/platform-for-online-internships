from backend.models import Subdivision
from tests.base import login_as, test_admin


def test_subdivisions_crud(db):
    client = login_as(test_admin)

    # create subdivision
    response = client.post('/api/subdivisions', json={
        'name': 'sub_1',
        'description': 'sub_1',
    })
    data = response.json()
    assert response.status_code == 200, data
    sub_1_id = data['id']
    assert data == {
        'id': sub_1_id,
        'name': 'sub_1',
        'description': 'sub_1',
    }

    # get list
    response = client.get('/api/subdivisions')
    data = response.json()
    assert response.status_code == 200, data
    assert data['total'] == 1
    assert data['items'][0] == {
        'id': sub_1_id,
        'name': 'sub_1',
    }

    # get one subdivision
    response = client.get(f'/api/subdivisions/{sub_1_id}')
    data = response.json()
    assert response.status_code == 200, data
    assert data == {
        'id': sub_1_id,
        'name': 'sub_1',
        'description': 'sub_1',
    }

    # patch subdivision
    response = client.patch(f'/api/subdivisions/{sub_1_id}', json={
        'name': 'new_sub_1',
    })
    data = response.json()
    assert response.status_code == 200, data
    assert data == {
        'id': sub_1_id,
        'name': 'new_sub_1',
        'description': 'sub_1',
    }

    # delete subdivision
    response = client.delete(f'/api/subdivisions/{sub_1_id}')
    assert response.status_code == 204
    assert db.query(Subdivision).all() == []
