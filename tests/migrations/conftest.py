import pytest
from sqlalchemy import create_engine

from staff.utils import alembic_config_from_url, tmp_database


@pytest.fixture
def postgres(pg_url):
    """
    Creates empty temporary database.
    """
    with tmp_database(pg_url, 'pytest') as tmp_url:
        yield tmp_url


@pytest.fixture()
def postgres_engine(postgres):
    """
    SQLAlchemy engine, bound to temporary database.
    """
    engine = create_engine(postgres, echo=True)
    try:
        yield engine
    finally:
        engine.dispose()


@pytest.fixture()
def alembic_config(postgres):
    """
    Alembic configuration object, bound to temporary database.
    """
    return alembic_config_from_url(postgres)
