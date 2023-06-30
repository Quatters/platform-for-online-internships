from sqlalchemy.orm import Session
from backend.models import User
from tests.base import login_as, test_admin, test_intern, test_teacher
from tests.helpers import create_user


def test_admin_cannot_use_chat():
    client = login_as(test_admin)
    response = client.get('/chat')
    assert response.status_code == 404

    response = client.post('/chat')
    assert response.status_code == 404


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
    with teacher_client.websocket_connect('/api/chat/ws') as ws:
        response = intern_client.post(f'/api/chat/{teacher.id}', json={'message': 'intern_1'})
        ws_data = ws.receive_json()
        assert ws_data == {
            'id': ws_data['id'],
            'message': 'intern_1',
            'created_at': ws_data['created_at'],
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
