import importlib
import os
from collections import namedtuple, defaultdict
from types import SimpleNamespace, ModuleType
from typing import List

from alembic.config import Config
from alembic.script import ScriptDirectory


MODULE_PATH = os.path.dirname(__file__)


def get_alembic_config(db_url: str) -> Config:
    cmd_options = SimpleNamespace(
        config=os.path.join(MODULE_PATH, 'alembic.ini'),
        db_url=db_url, name='alembic', raiseerr=False,
        rev_range=None, verbose=False, x=None,
    )

    config = Config(file_=cmd_options.config, cmd_opts=cmd_options)
    config.set_main_option('sqlalchemy.url', db_url)
    config.set_main_option('script_location', os.path.join(
        MODULE_PATH, 'alembic'
    ))

    return config


def get_revisions(db_url):
    revisions_dir = ScriptDirectory.from_config(get_alembic_config(db_url))
    for revision in revisions_dir.walk_revisions('base', 'heads'):
        yield revision


MigrationValidationParamsGroup = namedtuple('MigrationData', [
    'rev_base', 'rev_head', 'on_init', 'on_upgrade', 'on_downgrade'
])


def load_migration_as_module(file: str) -> ModuleType:
    return importlib.machinery.SourceFileLoader(
        file,
        os.path.join(MODULE_PATH, 'alembic', 'versions', file)
    ).load_module()


def make_validation_params_groups(
    *migrations: ModuleType
) -> List[MigrationValidationParamsGroup]:

    data = []
    for migration in migrations:

        # Ensure migration has all required params
        for required_param in ['rev_base', 'rev_head']:
            if not hasattr(migration, required_param):
                raise RuntimeError(
                    '{param} not specified for {migration}'.format(
                        param=required_param,
                        migration=migration.__name__
                    )
                )

        # Set up callbacks
        callbacks = defaultdict(lambda: lambda *args, **kwargs: None)
        for callback in ['on_init', 'on_upgrade', 'on_downgrade']:
            if hasattr(migration, callback):
                callbacks[callback] = getattr(migration, callback)

        data.append(
            MigrationValidationParamsGroup(
                rev_base=migration.rev_base,
                rev_head=migration.rev_head,
                on_init=callbacks['on_init'],
                on_upgrade=callbacks['on_upgrade'],
                on_downgrade=callbacks['on_downgrade']
            )
        )

    return data
