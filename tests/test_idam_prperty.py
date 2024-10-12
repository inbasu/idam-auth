import pytest

from idam.connection import IDAM


@pytest.fixture(scope="session")
def idam() -> IDAM:
    return IDAM()
