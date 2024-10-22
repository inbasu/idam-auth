import datetime
import time

import jwt
import pytest

from idam import TokenHandler


@pytest.fixture
def handler() -> TokenHandler:
    return TokenHandler(secret="secret", algorithm="HS256", lifetime=datetime.timedelta(seconds=3))


def test_create_token(handler) -> None:
    token = handler.generate_token({"hello": "world"})
    decoded = jwt.decode(token, key="secret", algorithms=["HS256"])
    assert decoded["hello"] == "world"


def test_decode_token(handler) -> None:
    token = handler.generate_token({"hello": "world"})
    assert jwt.decode(token, key="secret", algorithms=["HS256"]) == handler.decode_token(token)


def test_token_life_time(handler) -> None:
    token = handler.generate_token({"hello": "world"})
    time.sleep(3)
    result = handler.decode_token(token)
    assert result is None
