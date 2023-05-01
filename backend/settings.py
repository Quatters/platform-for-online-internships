import os
from pathlib import Path
from dotenv import load_dotenv

BACKEND_ROOT: Path = Path(__file__).parent.resolve().absolute()
PROJECT_ROOT: Path = BACKEND_ROOT.parent.absolute()

load_dotenv(PROJECT_ROOT / '.env')

if 'PYTEST_CURRENT_TEST' in os.environ:
    load_dotenv(PROJECT_ROOT / '.env.ci')

APP_NAME = 'platform_for_online_internships_backend'
API_VERSION = 'v1'
CLIENT_DOMAIN = os.getenv('CLIENT_DOMAIN', 'http://localhost:3000')

UVICORN_CONFIG = {
    'app': 'backend:app',
    'host': os.getenv('UVICORN_HOST', '0.0.0.0'),
    'port': int(os.getenv('UVICORN_PORT', 8000)),
    'reload': bool(os.getenv('UVICORN_HOT_RELOAD', False)),
}

STATIC_DIR = PROJECT_ROOT / 'static'
MEDIA_DIR = PROJECT_ROOT / 'media'

DATABASE_URL = os.environ['DATABASE_URL']

# python db clients usually are platform-dependent
# this solution is not very clean, but probably should work on linux & windows
if DATABASE_URL.startswith('mysql') or DATABASE_URL.startswith('mariadb'):
    import pymysql
    pymysql.install_as_MySQLdb()

AUTH = {
    'SECRET_KEY': os.environ['AUTH_SECRET_KEY'],
    'ALGORITHM': 'HS256',
    'TOKEN_EXPIRE_MINUTES': int(os.getenv('AUTH_TOKEN_EXPIRE_MINUTES', 30)),
    'TOKEN_URL': '/api/auth/token',
}
