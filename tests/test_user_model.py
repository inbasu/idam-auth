import pytest

from idam.model import User


@pytest.fixture(scope="module")
def user() -> User:
    return User(
        username="jone doe",
        email="hero@mail.com",
        roles=[],
        stores=[],
    )


def test_user_properties(user: User) -> None:
    assert hasattr(user, "username")
    assert hasattr(user, "email")
    assert hasattr(user, "roles")
