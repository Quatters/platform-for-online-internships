import orjson
from pathlib import Path
from fastapi.testclient import TestClient
from backend import app
from backend.settings import PROJECT_ROOT


client = TestClient(app)


def test_openapi_actuality():
    response = client.get('/openapi.json')
    assert response.status_code == 200

    server_openapi = response.json()
    file_openapi = orjson.loads((PROJECT_ROOT / 'openapi.json').read_bytes())

    for section in ('paths', 'components'):
        assert server_openapi[section] == file_openapi[section], (
            'Did you forget to regenerate schema? (Use python generate_openapi.py)',
        )
