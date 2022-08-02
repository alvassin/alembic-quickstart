"""
Test can find cases, when you've changed something in migration and forgot
about models for some reason (or vice versa).
"""
from alembic.command import upgrade
from alembic.config import Config
from sqlalchemy.engine.base import Engine
from alembic.runtime.migration import MigrationContext
from alembic.autogenerate import compare_metadata

from staff.schema import metadata


def test_migrations_up_to_date(
    alembic_config: Config,
    postgres_engine: Engine
):
    upgrade(alembic_config, 'head')

    migration_ctx = MigrationContext.configure(postgres_engine.connect())
    diff = compare_metadata(migration_ctx, metadata)
    assert not diff
