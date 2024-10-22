from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_auth_url() -> None:
    response = client.get("/login")
    assert response.status_code == 200


def test_whoami() -> None:
    response = client.get("/whoami")
    assert response.status_code == 200
