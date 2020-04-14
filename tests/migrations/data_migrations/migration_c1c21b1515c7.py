"""
Data migration test example.

MUST-have properties:
  - rev_base
    Previous migration identifier
  - rev_head
    Current (being tested) migration identifier

Optional properties:
  - on_init(engine)
    Is called before applying 'rev_head' migration. Can be used to add some
    data before migration is applied.
  - on_upgrade(engine)
    Is called after applying 'rev_head' migration. Can be used to check data
    was migrated successfully by upgrade() migration method.
  - on_downgrade(engine)
    Is called after migration is rolled back to 'rev_base'. Can be used to
    check data was rolled back to initial state.
"""

from sqlalchemy import Table, select
from sqlalchemy.engine import Engine

from staff.utils import load_migration_as_module


# Load migration as module
migration = load_migration_as_module('c1c21b1515c7_split_floor_and_seat.py')
rev_base: str = migration.down_revision
rev_head: str = migration.revision

# We can reuse objects from migration.
# users_table object with legacy & new columns would be very handy.
users_table: Table = migration.users_table

# Pytest call each test in separate process, so you could use global variables
# for this test to store state.
users = (
    {
        'user_id': 1,
        'email': 'john.smith@example.com',
        'name': 'John Smith',
        'gender': 'male',
        'location': '4.537',
        'floor': 4,
        'seat': 537,
    },
    {
        'user_id': 2,
        'email': 'josephine.smith@example.com',
        'name': 'Josephine Smith',
        'gender': 'female',
        'location': '1.1',
        'floor': 1,
        'seat': 1,
    },
)


def on_init(engine: Engine):
    """
    Create rows in users table before migration is applied
    """
    global users

    with engine.connect() as conn:
        query = users_table.insert().values([
            {
                'user_id': user['user_id'],
                'email': user['email'],
                'name': user['name'],
                'gender': user['gender'],
                'location': user['location'],
            }
            for user in users
        ])
        conn.execute(query)


def on_upgrade(engine: Engine):
    """
    Ensure that data was successfully migrated
    """
    global users

    with engine.connect() as conn:
        query = select([
            users_table.c.user_id,
            users_table.c.floor,
            users_table.c.seat
        ])

        actual = {
            user['user_id']: user
            for user in conn.execute(query).fetchall()
        }

        for user in users:
            assert user['user_id'] in actual
            assert user['floor'] == actual[user['user_id']]['floor']
            assert user['seat'] == actual[user['user_id']]['seat']


def on_downgrade(engine: Engine):
    """
    Ensure that data changes were rolled back
    """
    global users

    with engine.connect() as conn:
        query = select([
            users_table.c.user_id,
            users_table.c.location
        ])

        actual = {
            user['user_id']: user
            for user in conn.execute(query).fetchall()
        }

        for user in users:
            assert user['user_id'] in actual
            assert user['location'] == actual[user['user_id']]['location']
