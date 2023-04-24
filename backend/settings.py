import os
from pathlib import Path
from dotenv import load_dotenv

BACKEND_ROOT: Path = Path(__file__).parent.resolve().absolute()
PROJECT_ROOT: Path = BACKEND_ROOT.parent.absolute()

load_dotenv(PROJECT_ROOT / '.env')

APP_NAME = 'platform_for_online_internships_backend'
API_VERSION = 'v1'

UVICORN_CONFIG = {
    'app': 'backend.app:app',
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
