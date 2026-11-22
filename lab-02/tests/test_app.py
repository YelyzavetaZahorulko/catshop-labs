import pytest
import app as shop


@pytest.fixture
def client(monkeypatch, tmp_path):
    monkeypatch.setattr(shop, "DATABASE_URL", None)
    monkeypatch.setattr(
        shop, "COUNTER_FILE", tmp_path / "visits.txt"
    )

    shop.app.config["TESTING"] = True

    with shop.app.test_client() as test_client:
        yield test_client


def test_health(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.get_data(as_text=True) == "ok\n"


def test_ready(client):
    response = client.get("/ready")
    data = response.get_json()

    assert response.status_code == 200
    assert data["ready"] is True
    assert data["store"].startswith("file:")


def test_visits_starts_at_one(client):
    response = client.get("/visits")
    data = response.get_json()

    assert response.status_code == 200
    assert data["visits"] == 1


def test_visits_increments(client):
    first = client.get("/visits").get_json()
    second = client.get("/visits").get_json()

    assert first["visits"] == 1
    assert second["visits"] == 2


def test_visits_uses_file_storage(client):
    response = client.get("/visits")
    data = response.get_json()

    assert data["store"] == "file"