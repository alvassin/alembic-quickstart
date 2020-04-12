"""Initial migration

Revision ID: 5fd694768c6c
Revises:
Create Date: 2020-04-11 12:57:55.362843
"""

from alembic import op
from sqlalchemy import (
    Column, Enum, Integer, PrimaryKeyConstraint, String, UniqueConstraint
)


# revision identifiers, used by Alembic.
revision = '5fd694768c6c'
down_revision = None
branch_labels = None
depends_on = None


# We don't import GenderType fom staff.schema,
# because it may change from time to time.
GenderType = Enum('female', 'male', name='gender')


def upgrade():
    op.create_table(
        'users',
        Column('user_id', Integer(), nullable=False),
        Column('email', String(length=256), nullable=False),
        Column('name', String(collation='ru-RU-x-icu'), nullable=False),
        Column('gender', GenderType, nullable=False),
        Column('location', String(), nullable=False),
        PrimaryKeyConstraint('user_id', name=op.f('pk__users')),
        UniqueConstraint('email', name=op.f('uq__users__email'))
    )


def downgrade():
    op.drop_table('users')

    # Alembic won't delete gender data type, it should be done explicitly.
    GenderType.drop(op.get_bind(), checkfirst=False)
