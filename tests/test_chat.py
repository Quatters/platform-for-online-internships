from sqlalchemy.orm import Session
from backend.models import User
from tests.base import login_as, test_admin, test_intern, test_teacher


def test_admin_cannot_use_chat(db):
    client = login_as(test_admin)
    response = client.get('/api/chat/{intern.id}')
    intern = db.query(User).filter(User.email == test_intern.email).one()
    assert response.status_code == 403

    response = client.post(f'/api/chat/{intern.id}')
    assert response.status_code == 403


def test_invalid_chatters(db):
    client = login_as(test_intern)
    response = client.post('/api/chat/-1')
    data = response.json()
    assert response.status_code == 404, data

    teacher = db.query(User).filter(User.email == test_teacher.email).one()
    response = client.post(f'/api/chat/{teacher.id}')
    data = response.json()
    assert response.status_code == 404, data


def test_valid_chat(db: Session):
    intern = db.query(User).filter(User.email == test_intern.email).one()
    teacher = db.query(User).filter(User.email == test_teacher.email).one()
    intern.teacher = teacher
    db.commit()

    intern_client = login_as(test_intern)
    teacher_client = login_as(test_teacher)

    # get empty chat
    response = intern_client.get(f'/api/chat/{teacher.id}')
    data = response.json()
    assert response.status_code == 200, data
    assert data['total'] == 0

    response = teacher_client.get(f'/api/chat/{intern.id}')
    data = response.json()
    assert response.status_code == 200, data
    assert data['total'] == 0

    # create message as intern
    response = intern_client.post(f'/api/chat/{teacher.id}', json={'message': 'intern_1'})
    data = response.json()
    assert response.status_code == 200, data

    # get chats
    response = intern_client.get(f'/api/chat/{teacher.id}')
    data = response.json()
    assert response.status_code == 200, data
    assert data['total'] == 1
    assert data['items'] == [
        {
            'id': data['items'][0]['id'],
            'message': 'intern_1',
            'created_at': data['items'][0]['created_at'],
            'sender': {
                'id': intern.id,
                'email': intern.email,
                'first_name': intern.first_name,
                'last_name': intern.last_name,
                'patronymic': intern.patronymic,
            },
            'recipient': {
                'id': teacher.id,
                'email': teacher.email,
                'first_name': teacher.first_name,
                'last_name': teacher.last_name,
                'patronymic': teacher.patronymic,
            },
        }
    ]

    response = teacher_client.get(f'/api/chat/{intern.id}')
    data = response.json()
    assert response.status_code == 200, data
    assert data['total'] == 1
    assert data['items'][0]['message'] == 'intern_1'
    assert data['items'][0]['sender']['id'] == intern.id
    assert data['items'][0]['recipient']['id'] == teacher.id
