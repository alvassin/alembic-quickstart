Migrations testing and [Alembic](https://alembic.sqlalchemy.org/en/latest/) 
usage examples.

Prepared for ["Databases: models, migrations, testing"](https://habr.com/ru/company/yandex/blog/498856/#5) lection at 
[Yandex Backend Development school](https://yandex.ru/promo/academy/backend-school/) and 
["How to develop & test database migrations with Alembic"](https://youtu.be/qrlTDNaUQ-Q?t=5650) presentation at 
[Moscow Python meetup №69](https://events.yandex.ru/events/moscow-python-meetup-30-10-2019) (videos are in Russian). 

Code & examples are updated from time to time, please browse files at [7b804f8371bc14bbc35991654a37fc90b7fe4358](https://github.com/alvassin/alembic-quickstart/tree/7b804f8371bc14bbc35991654a37fc90b7fe4358) commit if you need exact code shown at Moscow Python meetup.

[🇷🇺 Russian translation](README_ru.md) is available for this document.

## What's inside

Aiohttp application with couple migrations and two commands: `staff-db` to control database state (Alembic wrapper) and `staff-api` (REST API aiohttp service).

Execute `make devenv` command to prepare development environment. It will create virtual environment in `./env` folder and install all dependencies (execute `make` for all available commands).

## How to control database state

Alembic provides `alembic` command to control database state (apply, rollback migrations, etc). In some cases it has the following disadvantages:

* `alembic` command requires `alembic.ini` configuration file, which is searched at current working directory. It is possible to specify path to `alembic.ini` using command-line argument `--config`, but it is easier to call the command from any folder without additional parameters.
* To connect Alembic to specific database it is required to change `sqlalachemy.url` parameter in `alembic.ini`. Sometimes (e.g. if the application is distributed via Docker container) it is much more convenient to specify the database URL with an environment variable and/or a command-line argument.
* Some applications need to extend standard Alembic arguments (e.g. to support working in different PostgreSQL schemas).

They can be solved by using Alembic wrapper. For example, `staff-db` provides ability to specify database URL using environment variable `STAFF_PG_URL` or `--pg-url` argument, resolves the path to `alembic.ini` using its location, rather than the current working directory.

## How to prepare database for tests

Very often tests require the database. You can create separate database for each test using pytest fixture (see [postgres fixture](tests/migrations/conftest.py#L8)), this approach allows to isolate tests from each other.

In most cases, tests require already prepared database with migrations applied. Since it is expensive to run migrations when creating a database for each test, you could do it once to prepare database, and then use it as template to create new databases.

Template database is created using [`migrated_postgres_template`](tests/api/conftest.py#L10) fixture within `session` scope. Databases for tests are created using [`migrated_postgres`](tests/api/conftest.py#L24) fixture.

## How to test migrations

### Stairway test
Simple and efficient method to check that migration does not have typos and 
rolls back all schema changes. Does not require maintenance - you can add this test 
to your project once and forget about it.

In particular, test detects the data types, that were previously created by `upgrade()` method 
and were not removed by `downgrade()`: when creating a table/column, Alembic automatically 
creates custom data types specified in columns (e.g. enum), but does not delete them when 
deleting table or column - developer has to do it manually.

#### How it works
Test retrieves all migrations list, and for each migration executes `upgrade`, 
`downgrade`, `upgrade` Alembic commands.
See [test_stairway.py](tests/migrations/test_stairway.py) for example.

<img src="assets/stairway.gif" width="800" height="277" alt="Stairway test">

### Data-migration test
Some migrations don't just add new columns or tables, but change the data in 
some way.

In addition to checking that the migration correctly rolls back changes to the 
data structure (stairway test), you need to check that the data is correctly 
changed by the `upgrade()` method and returned to the previous state by the 
`downgrade()` method.

This test does not guarantee that there are no bugs - it is very difficult to 
provide data sets for all cases. But data-altering migrations code is 
often very complex, errors are more common, and errors in such migrations can have 
the most serious consequences.

#### How it works

The test applies all migrations up to the one being tested and adds a dataset to the database that will be modified by the migration being tested.
Then test executes the `upgrade()` method and checks that the data was changed correctly. 
After this, test calls `downgrade()` method and checks that all data was returned to its initial state.
See [test_data_migrations.py](tests/migrations/test_data_migrations.py) for example.
