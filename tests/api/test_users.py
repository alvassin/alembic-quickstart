"""
Example of tests, that require database.

Separate database is created by `migrated_postgres` fixture for every test.

It works very fast even with many migrations: all hard work is done by fixture
`migrated_postgres_template` once per tests run, when `migrated_postgres`
fixture just clones ready database.
"""
from http import HTTPStatus

from staff.schema import Gender, users_table


USER = {
    'name': 'John Smith',
    'email': 'john.smith@example.com',
    'gender': Gender.male.value,
    'floor': 1,
    'seat': 1
}


async def test_create(api_client):
    response = await api_client.post('/users', json=USER)
    assert response.status == HTTPStatus.CREATED

    data = await response.json()
    for key, value in USER.items():
        assert value == data[key]


async def test_get(api_client):
    query = users_table.insert().values(USER)
    await api_client.app['pg'].execute(query)

    response = await api_client.get('/users')
    assert response.status == HTTPStatus.OK

    data = await response.json()
    assert len(data) == 1
    for key, value in USER.items():
        assert value == data[0][key]
