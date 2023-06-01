import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from fastapi import Query
from pydantic import Field
from fastapi_pagination import (
    LimitOffsetPage as LimitOffsetPageBase,
    LimitOffsetParams as LimitOffsetParamsBase,
)


BACKEND_ROOT: Path = Path(__file__).parent.resolve().absolute()
PROJECT_ROOT: Path = BACKEND_ROOT.parent.absolute()

load_dotenv(PROJECT_ROOT / '.env')

DEBUG = bool(os.getenv('DEBUG', False))

if 'pytest' in sys.modules:
    load_dotenv(PROJECT_ROOT / '.env.ci')

APP_NAME = 'platform_for_online_internships_backend'
API_VERSION = 'v1'
CLIENT_DOMAIN = os.getenv('CLIENT_DOMAIN', 'http://localhost:3000')

UVICORN_CONFIG = {
    'app': 'backend:app',
    'host': os.getenv('UVICORN_HOST', '0.0.0.0'),
    'port': int(os.getenv('UVICORN_PORT', 8000)),
    'reload': bool(os.getenv('UVICORN_HOT_RELOAD', False)),
    'log_level': 'debug' if DEBUG else 'info',
}

STATIC_DIR = PROJECT_ROOT / 'static'
MEDIA_DIR = PROJECT_ROOT / 'media'

for dir_ in (STATIC_DIR, MEDIA_DIR):
    if not dir_.exists():
        os.mkdir(dir_)

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


PAGINATION = {
    'DEFAULT_LIMIT': 20,
}

LimitOffsetPage = LimitOffsetPageBase.with_custom_options(
    limit=Field(PAGINATION['DEFAULT_LIMIT'], ge=1),
)


class LimitOffsetParams(LimitOffsetParamsBase):
    limit: int = Query(
        PAGINATION['DEFAULT_LIMIT'],
        ge=1,
        description='Page size limit',
    )
