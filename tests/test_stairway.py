import os

import pytest
from alembic.command import upgrade, downgrade
from sqlalchemy.engine import Engine, create_engine

from tests.conftest import DB_URL
from staff.testing import get_revisions, get_alembic_config


REVISIONS = list(get_revisions(DB_URL))
MODULE_PATH = os.path.dirname(os.path.dirname(__file__))


@pytest.mark.parametrize('rev_index', reversed(range(len(REVISIONS))))
def test_migrations_stairway(temp_db_engine: Engine, rev_index: int):
    revision = REVISIONS[rev_index]

    config = get_alembic_config(str(temp_db_engine.url))
    upgrade(config, revision.revision)
    downgrade(config, revision.down_revision or '-1')
    upgrade(config, revision.revision)
