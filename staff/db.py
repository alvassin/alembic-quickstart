"""
Alembic wrapper. Utility to manage database.
Unlike alembic command is available anywhere and can work in any folder.

Accepts --db-url argument (or STAFF_DB_URL env variable), that is used instead
of sqlalchemy.url option in alembic.ini
"""
import argparse
import logging
import os

from alembic.config import CommandLine

from staff.utils import DEFAULT_PG_URL, make_alembic_config


def main():
    logging.basicConfig(level=logging.DEBUG)

    alembic = CommandLine()
    alembic.parser.formatter_class = argparse.ArgumentDefaultsHelpFormatter
    alembic.parser.add_argument(
        '--pg-url', default=os.getenv('STAFF_PG_URL', DEFAULT_PG_URL),
        help='PostgreSQL URL [env: STAFF_PG_URL]'
    )

    options = alembic.parser.parse_args()
    if 'cmd' not in options:
        alembic.parser.error('too few arguments')
        exit(128)
    else:
        config = make_alembic_config(options)
        exit(alembic.run_cmd(config, options))


if __name__ == '__main__':
    main()
