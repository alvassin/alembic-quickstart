Contains examples how to test `Alembic`_ migrations.

Project was prepared for `Moscow Python meetup №69`_.

For details please see `video from meetup`_ (Russian language) on Youtube.


What's inside
-------------

There is small project called "staff" with a couple of migrations and tiny
aiohttp server.

To start using project execute ``make devenv``. It would create virtual
environment in env/ folder and install all dependencies (to see all available
commands call ``make``).

Project provides two utilities: ``staff-api`` (aiohttp server) and ``staff-db``
(alembic wrapper, tool for database management).

Main idea it that you can customize alembic as deep as you want.
For example, ``staff-db`` executable knows where is located alembic.ini
(unlike ``alembic`` executable), can be executed from any folder, and can accept
any additional arguments you may want.

Current version allows to use custom database url, instead of hardcoded
``sqlalchemy.url`` property in alembic.ini.

You can easily add ``--schema`` argument to execute migrations in separate
schema, etc.

There are two tests: stairway (``tests/test_stairway.py``) and test skeleton
for migrations with data (``tests/test_data_migrations.py``).

You may also find interesting how simple can be fixture ``temp_db``, that is creating
separate temporary database for each test and then dropping it.


.. _video from meetup: https://www.youtube.com/watch?v=qrlTDNaUQ-Q&feature=youtu.be&t=5862
.. _Alembic: https://alembic.sqlalchemy.org/en/latest/
.. _Moscow Python meetup №69: http://www.moscowpython.ru/meetup/69/talk-from-yandex/