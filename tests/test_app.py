from fastapi.testclient import TestClient

from app.main import create_app

client = TestClient(create_app())


def test_health() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_home_is_server_rendered() -> None:
    response = client.get("/")

    assert response.status_code == 200
    assert "Forfettario AI" in response.text
    assert "text/html" in response.headers["content-type"]
