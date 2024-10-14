import json

import pytest

from idam.idam import IDAM


@pytest.fixture
def token() -> bytes:
    with open("tests/token.json", "rb") as f:
        token = json.load(f)["token"]
    return token


@pytest.fixture(scope="session")
def idam() -> IDAM:
    return IDAM("clien_id", "client_secret", "redirect_uri", "realm_id")


def test_code_url(idam) -> None:
    assert (
        idam.code_url
        == "/authorize/api/oauth/authorization?response_type=code&redirect_uri=redirect_uri&client_id=clien_id&user_type=EMP&realm_id=realm_id&scope=clnt=clien_id"
    )


def test_decode_token(idam, token) -> None:
    decoded = idam.decode_token(token)
    assert decoded.get("email", False)
    assert decoded.get("authorization", False)


def test__get_stores(idam) -> None:
    assert idam._get_stores(
        {
            "MCC_RU_INSIGHT_STORE_ROLE": [
                {
                    "store": [
                        "14",
                        "372",
                        "9999",
                    ]
                }
            ]
        }
    ) == [
        "1014",
        "1372",
        "8001",
    ]


def test_create_user(idam, token: str) -> None:
    user = idam.create_user(idam.decode_token(token))
    assert user.email == "ivan.fisenko@metro-cc.ru"
    assert user.username == "ivan.fisenko"
    assert "MCC_RU_INSIGHT_IT_ROLE" in user.roles
    assert "1014" in user.store_role
