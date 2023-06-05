from tests.base import login_as, test_admin
from tests.helpers import create_competence, create_course, create_subdivision, get_records_count


def test_posts_crud():
    client = login_as(test_admin)

    #create post
    subdivision = create_subdivision()
    response = client.post(f'/api/subdivisions/{subdivision.id}/posts', json={
        'name': 'post_1',
        'description': 'post_1',
        'courses': [],
        'competencies': [],
    })
    data = response.json()
    assert response.status_code == 200, data
    post_1_id = data['id']


    #get post
    response = client.get(f'/api/subdivisions/{subdivision.id}/posts/{post_1_id}')
    data_2 = response.json()
    assert response.status_code == 200
    assert data == data_2


    #create post for another subdivision and get all posts
    all_posts_count = get_records_count(route='/api/posts', client=client)
    subdivision2 = create_subdivision()
    response = client.post(f'/api/subdivisions/{subdivision2.id}/posts', json={
        'name': 'post_2',
        'description': 'post_2',
        'courses': [],
        'competencies': [],
    })
    data = response.json()
    assert response.status_code == 200, data
    response = client.get('/api/posts')
    data = response.json()
    assert len(data['items']) == all_posts_count + 1


    #create another post in the same subdivision and get all posts in it
    posts_in_subdivision_count = get_records_count(route=f'/api/subdivisions/{subdivision.id}/posts',
                                                   client=client)
    response = client.post(f'/api/subdivisions/{subdivision.id}/posts', json={
        'name': 'post_3',
        'description': 'post_3',
        'courses': [],
        'competencies': [],
    })
    data = response.json()
    assert response.status_code == 200, data
    response = client.get(f'/api/subdivisions/{subdivision.id}/posts')
    data = response.json()
    assert response.status_code == 200, data
    assert len(data['items']) == posts_in_subdivision_count + 1


    # add competencies to post
    competence = create_competence()
    response = client.patch(f'/api/subdivisions/{subdivision.id}/posts/{post_1_id}', json={
        'competencies': [competence.id]
    })
    data = response.json()
    assert response.status_code == 200
    assert len(data['competencies']) == 1


    #add courses to post
    course = create_course()
    response = client.patch(f'/api/subdivisions/{subdivision.id}/posts/{post_1_id}', json={
        'courses': [course.id]
    })
    data = response.json()
    assert response.status_code == 200
    assert len(data['courses']) == 1


    #delete post
    posts_in_subdivision_count = get_records_count(route=f'/api/subdivisions/{subdivision.id}/posts',
                                                   client=client)
    response = client.delete(f'/api/subdivisions/{subdivision.id}/posts/{post_1_id}')
    assert response.status_code == 204
    response = client.get(f'/api/subdivisions/{subdivision.id}/posts/')
    data = response.json()
    assert response.status_code == 200, data
    assert len(data['items']) == posts_in_subdivision_count - 1
