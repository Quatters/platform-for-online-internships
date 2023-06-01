from tests.base import login_as, test_admin, client


def test_get_token():
    auth_data = {
        'username': test_admin.email,
        'password': test_admin.password,
    }
    response = client.post('/api/auth/token', data=auth_data, headers={
        'Content-Type': 'application/x-www-form-urlencoded',
    })
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


def test_example():
    client = login_as(test_admin)
    response = client.get('/api/users/me')
    assert response.status_code == 200
