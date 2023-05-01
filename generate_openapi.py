import orjson
from fastapi.openapi.utils import get_openapi
from backend import app
from backend.settings import PROJECT_ROOT, API_VERSION


schema = get_openapi(
    title='Platform for online internships',
    routes=app.routes,
    version=API_VERSION,
)
json_schema = orjson.dumps(schema, option=orjson.OPT_INDENT_2)
(PROJECT_ROOT / 'openapi.json').write_bytes(json_schema)

print('Done.')
