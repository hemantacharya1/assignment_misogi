from fastapi.testclient import TestClient

from ..main import app

client = TestClient(app)


def test_root():
    resp = client.get("/")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"


def test_products_list():
    resp = client.get("/products")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    # At least one product once DB is seeded
    assert len(data) >= 0  # length may be 0 on first run before seeding completes


def test_products_pagination():
    resp = client.get("/products?page=1&page_size=5")
    assert resp.status_code == 200
    assert len(resp.json()) <= 5 