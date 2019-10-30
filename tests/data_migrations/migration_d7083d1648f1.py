import sqlalchemy as sa
from sqlalchemy.engine import Engine

from staff.testing import load_migration_as_module


# Load migration as module
migration = load_migration_as_module(
    'd7083d1648f1_added_name_and_surname.py'
)

rev_base = migration.down_revision
rev_head = migration.revision


def on_init(engine: Engine):
    """
    Create database entries before migration is applied
    """
    with engine.connect() as conn:
        print('on_init')
        # insert data to the database


def on_upgrade(engine: Engine):
    """
    Ensure that data is successfully migrated
    """
    with engine.connect() as conn:
        print('on_upgrade')
        # check data was migrated correctly


def on_downgrade(engine: Engine):
    """
    Ensure that attrs2measures entry is present after downgrade
    """
    with engine.connect() as conn:
        print('on_downgrade')
        # check data was downgraded correctly
