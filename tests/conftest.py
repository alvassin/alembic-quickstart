import os
import uuid

import pytest
from sqlalchemy import create_engine
from sqlalchemy_utils import create_database, drop_database
from yarl import URL

from staff.utils import DEFAULT_PG_URL, alembic_config_from_url


PG_URL = os.getenv('CI_STAFF_PG_URL', DEFAULT_PG_URL)


@pytest.fixture
def postgres():
    """
    Creates temporary database for each test and then drops it.

    If there are connected clients when test is finished -
    disconnects them before dropping table.
    """
    tmp_name = '.'.join([uuid.uuid4().hex, 'pytest'])
    tmp_url = str(URL(PG_URL).with_path(tmp_name))
    create_database(tmp_url)

    try:
        yield tmp_url
    finally:
        drop_database(tmp_url)


@pytest.fixture()
def postgres_engine(postgres):
    """
    Engine, bound to temporary database.
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
