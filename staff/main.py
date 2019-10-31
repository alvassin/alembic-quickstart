from functools import partial

from aiohttp.web import Application, run_app
from aiohttp.web_exceptions import HTTPBadRequest
from aiohttp.web_response import json_response
from asyncpgsa import PG
from configargparse import ArgumentParser
from yarl import URL

from staff.schema import users_table

# ConfigArgParse allows to use env variables in addition to arguments.
# E.g. you may configure your server using STAFF_HOST, STAFF_PORT, STAFF_DB_URL
# env vars.
parser = ArgumentParser(auto_env_var_prefix='STAFF_')
parser.add_argument('--host', type=str, default='127.0.0.1',
                    help='Host to listen')
parser.add_argument('--port', type=int, default=8080,
                    help='Port to listen')
parser.add_argument(f'--db-url', type=URL,
                    default=URL('postgresql://staff:hackme@0.0.0.0/staff'),
                    help='URL to use to connect to the database')


async def init_pg(app, db_url):
    """
    Init asyncpgsa driver (asyncpg + sqlalchemy)
    """
    app['pg'] = PG()
    await app['pg'].init(db_url)


async def handle_get_users(request):
    """
    Return existing users
    """
    rows = await request.app['pg'].fetch(users_table.select())
    return json_response([dict(row) for row in rows])


async def handle_create_user(request):
    """
    Create new user
    """
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
    """
    Run application.
    Is called via command-line env/bin/staff-api, created by setup.py.
    """
    args = parser.parse_args()

    app = Application()
    app.router.add_route('GET', '/users', handle_get_users)
    app.router.add_route('POST', '/users', handle_create_user)
    app.on_startup.append(
        partial(init_pg, db_url=str(args.db_url))
    )
    run_app(app, host=args.host, port=args.port)
