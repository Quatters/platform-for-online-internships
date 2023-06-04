from backend.database import get_db
from backend.models import User
from tests.base import login_as, test_admin, test_intern, test_anonymous


def test_get_token():
    auth_data = {
        'username': test_admin.email,
        'password': test_admin.password,
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    client = login_as(test_anonymous)

    # check invalid password
    response = client.post(
        '/api/auth/token',
        data={**auth_data, 'password': 'invalid'},
        headers=headers,
    )
    assert response.status_code == 401

    # check invalid email
    response = client.post(
        '/api/auth/token',
        data={**auth_data, 'username': 'invalid'},
        headers=headers,
    )
    assert response.status_code == 401

    # check valid credentials
    response = client.post('/api/auth/token', data=auth_data, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data['token_type'] == 'bearer'
    assert data['access_token']

    response = client.get('/api/users/me', headers={
        'Authorization': f'Bearer {data["access_token"]}'
    })
    assert response.status_code == 200
    data = response.json()
    assert_user = {
        **test_admin.dict(),
        'posts': [],
    }
    assert type(data['id']) == int
    del data['id']
    del assert_user['password']
    assert data == assert_user


def test_get_list_users():
    client = login_as(test_admin)
    response = client.get('/api/users')
    assert response.status_code == 200
    data = response.json()
    assert data['total'] == 3, data

    # check search
    response = client.get('/api/users?search=ter')
    assert response.status_code == 200
    data = response.json()
    assert data['total'] == 1
    assert data['items'][0]['email'] == 'intern@test.com'


def test_only_admin_can_update_user():
    client = login_as(test_admin)
    teacher = next(get_db()).query(User).filter(User.is_teacher).one()

    response = client.get(f'/api/users/{teacher.id}')
    assert response.status_code == 200
    assert response.json()['first_name'] == ''

    response = client.patch(f'/api/users/{teacher.id}', json={
        'first_name': 'Teacher 1',
    })
    assert response.status_code == 200

    response = client.get(f'/api/users/{teacher.id}')
    assert response.status_code == 200
    assert response.json()['first_name'] == 'Teacher 1'

    # check cannot update with other user's email
    response = client.patch(f'/api/users/{teacher.id}', json={
        'email': 'admin@test.com',
    })
    assert response.status_code == 400
    assert response.json()['code'] == 'integrity_error'

    client = login_as(test_intern)
    response = client.get(f'/api/users/{teacher.id}')
    assert response.status_code == 200

    response = client.patch(f'/api/users/{teacher.id}')
    assert response.status_code == 403
    assert response.json() == {'detail': 'Operation not permitted.'}


def test_get_invalid_user():
    client = login_as(test_admin)
    response = client.get('/api/users/-1')
    assert response.status_code == 404
    assert response.json()['detail'] == 'Not found.'


def test_update_user_posts():
    client = login_as(test_admin)
    teacher = next(get_db()).query(User).filter(User.is_teacher).one()

    # try to add invalid post
    response = client.patch(f'/api/users/{teacher.id}', json={
        'posts': [-1],
    })
    assert response.status_code == 400
    assert response.json()['detail'] == 'Some of the instances not exist.'

    # create subdivision
    response = client.post('/api/subdivisions', json={
        'name': 'subdivision_1',
        'description': '123',
    })
    assert response.status_code == 200
    data = response.json()
    sub_id = data['id']

    # create post
    response = client.post(f'/api/subdivisions/{sub_id}/posts', json={
        'name': 'post_1',
        'description': '123',
        'courses': [],
    })
    assert response.status_code == 200
    data = response.json()
    post_id = data['id']

    # add post
    response = client.patch(f'/api/users/{teacher.id}', json={
        'posts': [post_id],
    })
    assert response.status_code == 200
    response = client.get(f'/api/users/{teacher.id}')
    assert response.status_code == 200
    assert response.json()['posts'] == [
        {'id': post_id, 'name': 'post_1'},
    ]
