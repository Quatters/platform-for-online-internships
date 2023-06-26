import pytest
import alembic.command
import alembic.config
from sqlalchemy_utils import drop_database, create_database, database_exists
from backend.settings import PROJECT_ROOT
from backend.database import engine, get_db
from backend import app
from tests.base import create_user, test_admin, test_teacher, test_intern

from sqlalchemy import event
from sqlalchemy.orm import sessionmaker


TestSession = sessionmaker(autoflush=False, autocommit=False)
alembic_config = alembic.config.Config(str(PROJECT_ROOT / 'alembic.ini'))


@pytest.fixture(scope='session', autouse=True)
def initialize_session():
    if database_exists(engine.url):
        drop_database(engine.url)
    create_database(engine.url)

    connection = engine.connect()
    alembic_config.attributes['connection'] = connection
    alembic.command.upgrade(alembic_config, 'head')
    connection.commit()

    try:
        yield
    finally:
        drop_database(engine.url)
        connection.close()


@pytest.fixture(scope='session', autouse=True)
def populate_test_users(initialize_session):
    with engine.connect() as connection:
        session = TestSession(bind=connection)
        session.bulk_save_objects([
            create_user(session, user=user, commit=False)
            for user in (test_admin, test_teacher, test_intern)
        ])
        session.commit()
        session.close()


@pytest.fixture(scope='function', autouse=True)
def db():
    connection = engine.connect()
    transaction = connection.begin()
    session = TestSession(bind=connection)
    savepoint = session.begin_nested()

    @event.listens_for(session, 'after_transaction_end')
    def end_savepoint(session, transaction):
        nonlocal savepoint
        if not savepoint.is_active:
            savepoint = connection.begin_nested()

    def override_get_db():
        nonlocal session, savepoint
        try:
            yield session
        except:  # noqa: E722
            session.rollback()
            savepoint = connection.begin_nested()

    app.dependency_overrides[get_db] = override_get_db

    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()
