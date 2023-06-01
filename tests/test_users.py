from tests.base import test_admin
from tests.utils import login_as


def test_example():
    client = login_as(test_admin)
    response = client.get('/api/users/me')
    assert response.status_code == 200
