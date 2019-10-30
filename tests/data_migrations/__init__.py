from staff.testing import make_validation_params_groups
from . import (
    migration_d7083d1648f1,
)

VALIDATION_PARAM_GROUPS = make_validation_params_groups(
    migration_d7083d1648f1,
)


__all__ = (
    'VALIDATION_PARAM_GROUPS',
)
