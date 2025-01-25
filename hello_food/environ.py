from typing import Final

import os

"""
The PG database hostname.
"""
POSTGRES_HOSTNAME = os.getenv("POSTGRES_HOSTNAME") or "randi1-5.local"

"""
Set by pytest when running tests.
See: https://docs.pytest.org/en/latest/reference/reference.html#envvar-PYTEST_VERSION
"""
PYTEST_VERSION: Final[str | None] = os.getenv("PYTEST_VERSION")

"""
Indicates that the application is being run within CI when set.
"""
CI: Final[str | None] = os.getenv("CI")

"""
Indicates that the application is running in a production environment when
set.
"""
PROD: Final[str | None] = os.getenv("PROD")
