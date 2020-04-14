from functools import partial
from http import HTTPStatus

from aiohttp.web import Application, run_app
from aiohttp.web_exceptions import HTTPBadRequest
from aiohttp.web_response import json_response
from asyncpg import NotNullViolationError
from asyncpgsa import PG
from configargparse import ArgumentParser
from yarl import URL

from staff.schema import users_table
from staff.utils import DEFAULT_PG_URL


# ConfigArgParse allows to use env variables in addition to arguments.
# E.g. you may configure your server using STAFF_HOST, STAFF_PORT, STAFF_DB_URL
# env vars.
parser = ArgumentParser(auto_env_var_prefix='STAFF_')
parser.add_argument('--host', type=str, default='127.0.0.1',
                    help='Host to listen')
parser.add_argument('--port', type=int, default=8080,
                    help='Port to listen')
parser.add_argument('--pg-url', type=URL, default=URL(DEFAULT_PG_URL),
                    help='URL to use to connect to the postgres database')


async def init_pg(app, pg_url):
    """
    Init asyncpgsa driver (asyncpg + sqlalchemy)
    """
    app['pg'] = PG()
    await app['pg'].init(pg_url)
    try:
        yield
    finally:
        await app['pg'].pool.close()


async def handle_get_users(request):
    """
    Handler, returns existing users
    """
    rows = await request.app['pg'].fetch(users_table.select())
    return json_response([dict(row) for row in rows])


async def handle_create_user(request):
    """
    Handler, creates new user
    """
    data = await request.json()

    try:
        query = users_table.insert().values(
            email=data['email'],
            name=data.get('name'),
            gender=data.get('gender'),
            floor=data.get('floor'),
            seat=data.get('seat')
        ).returning(users_table)
        row = await request.app['pg'].fetchrow(query)
        return json_response(dict(row), status=HTTPStatus.CREATED)
    except NotNullViolationError:
        raise HTTPBadRequest()


def create_app(pg_url) -> Application:
    app = Application()
    app.cleanup_ctx.append(partial(init_pg, pg_url=str(pg_url)))
    app.router.add_route('GET', '/users', handle_get_users)
    app.router.add_route('POST', '/users', handle_create_user)
    return app


def main():
    """
    Run application.
    Is called via command-line env/bin/staff-api, created by setup.py.
    """
    args = parser.parse_args()
    app = create_app(args.pg_url)
    run_app(app, host=args.host, port=args.port)


if __name__ == '__main__':
    main()
