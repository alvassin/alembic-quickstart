import sqlalchemy
from sqlalchemy import Table, Column, Integer, String, Boolean, text, DateTime

RU_COLLATION = 'ru-RU-x-icu'


convention = {
    'all_column_names': lambda constraint, table: '_'.join([
        column.name for column in constraint.columns.values()
    ]),
    'ix': 'ix__%(table_name)s__%(all_column_names)s',
    'uq': 'uq__%(table_name)s__%(all_column_names)s',
    'ck': 'ck__%(table_name)s__%(constraint_name)s',
    'fk': (
        'fk__%(table_name)s__%(all_column_names)s__'
        '%(referred_table_name)s'
    ),
    'pk': 'pk__%(table_name)s'
}

metadata = sqlalchemy.MetaData(naming_convention=convention)


users_table = Table(
    'users',
    metadata,
    Column('user_id', Integer, primary_key=True),
    Column('email', String(256), nullable=False, unique=True),
    Column('name', String(256, collation=RU_COLLATION), nullable=True),
    Column('surname', String(256, collation=RU_COLLATION), nullable=True)
)
