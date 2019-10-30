from typing import Callable

import pytest
from alembic.command import downgrade, upgrade
from sqlalchemy.engine import Engine

from staff.testing import get_alembic_config, get_revisions
from tests import data_migrations
from tests.conftest import DB_URL


REVISIONS = list(get_revisions(DB_URL))


@pytest.mark.parametrize(
    ['rev_base', 'rev_head', 'on_init', 'on_upgrade', 'on_downgrade'],
    data_migrations.VALIDATION_PARAM_GROUPS
)
def test_data_migrations(
    temp_db_engine: Engine, rev_base: str, rev_head: str,
    on_init: Callable, on_upgrade: Callable, on_downgrade: Callable
):
    """
    Check data is migrated correctly in "data" migrations.
    """
    config = get_alembic_config(str(temp_db_engine.url))

    upgrade(config, rev_base)
    on_init(engine=temp_db_engine)

    upgrade(config, rev_head)
    on_upgrade(engine=temp_db_engine)

    downgrade(config, rev_base)
    on_downgrade(engine=temp_db_engine)