import os
import uuid

import pytest
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy_utils import create_database, drop_database
from yarl import URL


DB_URL = os.getenv('CI_STAFF_DB_URL',
                   'postgresql://staff:hackme@0.0.0.0/staff')


@pytest.fixture
def temp_db() -> str:
    """
    Создает временную базу данных для теста и потом удаляет ее, отключая всех
    клиентов (если по какой-то причине не все отключились)
    """
    tmp_db_name = '.'.join([uuid.uuid4().hex, 'pytest'])
    tmp_db_url = str(URL(DB_URL).with_path(tmp_db_name))
    create_database(tmp_db_url)

    try:
        yield tmp_db_url
    finally:
        drop_database(tmp_db_url)


@pytest.fixture()
def temp_db_engine(temp_db) -> Engine:
    engine = create_engine(temp_db, echo=True)
    try:
        yield engine
    finally:
        engine.dispose()
