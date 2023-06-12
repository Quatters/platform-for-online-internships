from backend.database import get_db
from backend.models import User
from tests.base import login_as, test_admin, test_intern, test_anonymous
from tests import helpers


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
        'teacher': None,
        'interns': [],
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


def test_create_user():
    client = login_as(test_admin)

    subdivision = helpers.create_subdivision()
    post_1 = helpers.create_post(subdivision_id=subdivision.id)
    post_2 = helpers.create_post(subdivision_id=subdivision.id)

    # create intern
    response = client.post('/api/users', json={
        'first_name': 'Intern',
        'email': 'some_intern@test.com',
        'password': '12345',
        'posts': [
            post_1.id,
            post_2.id,
        ],
        'is_teacher': False,
        'is_admin': False,
    })
    data = response.json()
    assert response.status_code == 200, data
    response = client.get('/api/users')
    data = response.json()
    assert response.status_code == 200
    assert data['total'] == 4

    # check that user can login
    auth_data = {
        'username': 'some_intern@test.com',
        'password': '12345',
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    intern_client = login_as(test_anonymous)
    response = intern_client.post('/api/auth/token', data=auth_data, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data['token_type'] == 'bearer'
    assert data['access_token']

    response = intern_client.get('/api/users/me', headers={
        'Authorization': f'Bearer {data["access_token"]}'
    })
    data = response.json()
    assert response.status_code == 200, data
    assert data['email'] == 'some_intern@test.com'
    assert data['posts'] == [
        {'id': post_1.id, 'name': post_1.name},
        {'id': post_2.id, 'name': post_2.name},
    ]


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
        'competencies': [],
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


def test_assign_interns_to_teacher():
    admin_client = login_as(test_admin)
    db = next(get_db())

    teacher_1 = helpers.create_user(is_teacher=True, db=db)
    teacher_2 = helpers.create_user(is_teacher=True, db=db)

    intern_1 = helpers.create_user(db=db)
    intern_2 = helpers.create_user(db=db)
    intern_3 = helpers.create_user(db=db)
    intern_4 = helpers.create_user(db=db)

    subdivision = helpers.create_subdivision()
    post_1 = helpers.create_post(subdivision_id=subdivision.id, db=db)
    post_2 = helpers.create_post(subdivision_id=subdivision.id, db=db)

    teacher_1.posts = [post_1, post_2]
    teacher_2.posts = [post_1]
    intern_1.posts = [post_1]
    intern_2.posts = [post_1, post_2]
    intern_4.posts = [post_2]
    db.commit();

    # check 404 for intern
    response = admin_client.get(f'/api/users/{intern_1.id}/assigned_interns')
    assert response.status_code == 404

    # check empty list
    response = admin_client.get(f'/api/users/{teacher_1.id}/assigned_interns')
    data = response.json()
    assert response.status_code == 200, data
    assert data['total'] == 0
    assert data['items'] == []

    # assign intern_1, intern_2 to teacher_1
    response = admin_client.put(f'/api/users/{teacher_1.id}/assigned_interns', json={
        'interns': [intern_1.id, intern_2.id],
    })
    data = response.json()
    assert response.status_code == 200, data
    response = admin_client.get(f'api/users/{teacher_1.id}/assigned_interns')
    data = response.json()
    assert response.status_code == 200, data
    assert data['total'] == 2
    assert data['items'][0]['id'] == intern_1.id
    assert data['items'][1]['id'] == intern_2.id

    # try to assign intern_3 to teacher_1
    response = admin_client.put(f'/api/users/{teacher_1.id}/assigned_interns', json={
        'interns': [intern_3.id],
    })
    data = response.json()
    assert response.status_code == 400
    assert data['detail'] == (
        f'Intern {intern_3.email} (id: {intern_3.id}) cannot be assigned to this teacher because they have no '
        'matching posts.'
    )

    # check that all as before
    response = admin_client.get(f'api/users/{teacher_1.id}/assigned_interns')
    data = response.json()
    assert response.status_code == 200
    assert data['total'] == 2

    # try to reassign intern_1 to teacher_2
    response = admin_client.put(f'/api/users/{teacher_2.id}/assigned_interns', json={
        'interns': [intern_1.id],
    })
    data = response.json()
    assert response.status_code == 400, data
    assert data['detail'] == 'One or more of the interns are already assigned to teacher.'

    # get intern_1
    response = admin_client.get(f'/api/users/{intern_1.id}')
    data = response.json()
    assert response.status_code == 200, data
    assert data == {
        'id': intern_1.id,
        'email': intern_1.email,
        'first_name': intern_1.first_name,
        'last_name': intern_1.last_name,
        'patronymic': intern_1.patronymic,
        'is_admin': False,
        'is_teacher': False,
        'teacher': {'id': teacher_1.id, 'email': teacher_1.email},
        'interns': [],
        'posts': [
            {'id': post_1.id, 'name': post_1.name},
        ],
    }
    # get teacher_1
    response = admin_client.get(f'/api/users/{teacher_1.id}')
    data = response.json()
    assert response.status_code == 200, data
    assert data == {
        'id': teacher_1.id,
        'email': teacher_1.email,
        'first_name': teacher_1.first_name,
        'last_name': teacher_1.last_name,
        'patronymic': teacher_1.patronymic,
        'is_admin': False,
        'is_teacher': True,
        'teacher': None,
        'interns': [
            {'id': intern_1.id, 'email': intern_1.email},
            {'id': intern_2.id, 'email': intern_2.email},
        ],
        'posts': [
            {'id': post_1.id, 'name': post_1.name},
            {'id': post_2.id, 'name': post_2.name},
        ],
    }

    # get unassigned interns to teacher_1
    response = admin_client.get(f'/api/users/{teacher_1.id}/suitable_for_assign_interns')
    data = response.json()
    assert response.status_code == 200, data
    assert data['total'] == 1
    assert data['items'][0] == {
        'id': intern_4.id,
        'email': intern_4.email,
    }

    # get unassigned interns to teacher_2
    response = admin_client.get(f'/api/users/{teacher_2.id}/suitable_for_assign_interns')
    data = response.json()
    assert response.status_code == 200, data
    assert data['total'] == 0
