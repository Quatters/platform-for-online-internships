import pytest
import alembic.command
import alembic.config
from backend.settings import PROJECT_ROOT
from backend.database import engine


@pytest.fixture(scope='function', autouse=True)
def run_migrations():
    config = alembic.config.Config(str(PROJECT_ROOT / 'alembic.ini'))
    with engine.begin() as connection:
        config.attributes['connection'] = connection
        alembic.command.upgrade(config, 'head')
        connection.commit()
        yield None
        alembic.command.downgrade(config, 'base')
