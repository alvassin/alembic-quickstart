from aiohttp.web import Application, Response, run_app
from aiohttp.web_exceptions import HTTPBadRequest
from aiohttp.web_response import json_response
from asyncpgsa import PG

from staff.schema import users_table


async def init_pg(app):
    app['pg'] = PG()
    await app['pg'].init('postgresql://staff:hackme@0.0.0.0/staff')


async def handle_get_users(request):
    rows = await request.app['pg'].fetch(users_table.select())
    return json_response([dict(row) for row in rows])


async def handle_create_user(request):
    data = await request.json()
    if 'email' not in data:
        raise HTTPBadRequest()

    query = users_table.insert().values(
        email=data['email'],
        name=data.get('name'),
        surname=data.get('surname')
    ).returning(users_table)
    row = await request.app['pg'].fetchrow(query)
    return json_response(dict(row))


def main():
    app = Application()
    app.router.add_route('GET', '/users', handle_get_users)
    app.router.add_route('POST', '/users', handle_create_user)
    app.on_startup.append(init_pg)
    run_app(app, port=8081)


