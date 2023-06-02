import pytest
import alembic.command
import alembic.config
from sqlalchemy_utils import drop_database, create_database, database_exists
from backend.settings import PROJECT_ROOT
from backend.database import engine, get_db
from tests.base import create_user, test_admin, test_teacher, test_intern


db_connection = None


@pytest.fixture(scope='session', autouse=True)
def initialize_session():
    config = alembic.config.Config(str(PROJECT_ROOT / 'alembic.ini'))

    if database_exists(engine.url):
        drop_database(engine.url)
    create_database(engine.url)

    db_connection = engine.connect()
    config.attributes['connection'] = db_connection
    alembic.command.upgrade(config, 'head')
    db_connection.commit()

    session = next(get_db())
    for user in (test_admin, test_teacher, test_intern):
        create_user(user, db=session)
    session.commit()

    try:
        yield
    finally:
        drop_database(engine.url)
        db_connection.close()


@pytest.fixture(scope='function', autouse=True)
def rollback_db():
    yield
    if db_connection:
        db_connection.rollback()
