"""Split location into floor and seat columns

Revision ID: c1c21b1515c7
Revises: 5fd694768c6c
Create Date: 2020-04-11 13:06:48.414125
"""

from alembic import op
from sqlalchemy import (
    Column, Enum, Integer, MetaData, PrimaryKeyConstraint, SmallInteger,
    String, Table, UniqueConstraint, cast, func
)


# revision identifiers, used by Alembic.
revision = 'c1c21b1515c7'
down_revision = '5fd694768c6c'
branch_labels = None
depends_on = None


LOCATION_DELIMETER = '.'

metadata = MetaData()
users_table = Table(
    'users',
    metadata,
    Column('user_id', Integer(), nullable=False),
    Column('email', String(length=256), nullable=False),
    Column('name', String(collation='ru-RU-x-icu'), nullable=False),
    Column('gender', Enum('female', 'male', name='gender'), nullable=False),
    Column('location', String(), nullable=False),
    Column('floor', SmallInteger(), nullable=False),
    Column('seat', SmallInteger(), nullable=False),
    PrimaryKeyConstraint('user_id', name='pk__users'),
    UniqueConstraint('email', name='uq__users__email')
)


def upgrade():
    # Add new nullable columns
    op.add_column('users', Column('floor', SmallInteger(), nullable=True))
    op.add_column('users', Column('seat', SmallInteger(), nullable=True))

    # Migrate data
    query = users_table.update().values(
        floor=cast(
            func.split_part(users_table.c.location, LOCATION_DELIMETER, 1),
            Integer
        ),
        seat=cast(
            func.split_part(users_table.c.location, LOCATION_DELIMETER, 2),
            Integer
        )
    )
    op.execute(query)

    # Make new columns non-nullable
    op.alter_column('users', 'floor', nullable=False)
    op.alter_column('users', 'seat', nullable=False)

    # Drop legacy column
    op.drop_column('users', 'location')


def downgrade():
    # Add legacy nullable column
    op.add_column('users', Column('location', String(), nullable=True))

    # Migrate data
    query = users_table.update().values(
        location=func.concat(
            cast(users_table.c.floor, String),
            LOCATION_DELIMETER,
            cast(users_table.c.seat, String)
        )
    )
    op.execute(query)

    # Make legacy column non-nullable
    op.alter_column('users', 'location', nullable=False)

    # Drop new columns
    op.drop_column('users', 'seat')
    op.drop_column('users', 'floor')
