"""
Alembic wrapper. Utility to manage database.
Unlike alembic command is available anywhere and can work in any folder.

Accepts --db-url argument (or STAFF_DB_URL env variable), that is used instead
of sqlalchemy.url option in alembic.ini
"""
import logging
import os

from alembic.config import CommandLine, Config


MODULE_PATH = os.path.dirname(__file__)


def main():
    current_dir = os.path.abspath(os.getcwd())

    try:
        logging.basicConfig(level=logging.DEBUG)
        alembic = CommandLine()
        alembic.parser.add_argument(
            '--db-url', default=os.getenv('STAFF_DB_URL'),
            help='Database URL [env: STAFF_DB_URL]'
        )

        options = alembic.parser.parse_args()

        if not options.db_url:
            alembic.parser.error('--db-url is required')
            exit(127)

        if options.config == 'alembic.ini':
            options.config = os.path.join(MODULE_PATH, options.config)

        cfg = Config(
            file_=options.config,
            ini_section=options.name,
            cmd_opts=options
        )

        cfg.set_main_option('script_location',
                            str(os.path.join(MODULE_PATH, 'alembic')))
        cfg.set_main_option('sqlalchemy.url', options.db_url)

        if 'cmd' not in options:
            alembic.parser.error('please specify command')
            exit(128)
        else:
            exit(alembic.run_cmd(cfg, options))
    finally:
        os.chdir(current_dir)