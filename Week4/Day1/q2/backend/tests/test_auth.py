from fastapi.testclient import TestClient

from ..main import app

client = TestClient(app)

TEST_EMAIL = "test@example.com"
TEST_PASSWORD = "secret123"


def test_register_and_login():
    # Register
    resp = client.post("/auth/register", json={"email": TEST_EMAIL, "password": TEST_PASSWORD})
    assert resp.status_code in (201, 400)  # 400 if already exists from previous run

    # Login
    resp = client.post(
        "/auth/login",
        data={"username": TEST_EMAIL, "password": TEST_PASSWORD},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert resp.status_code == 200
    token = resp.json()["access_token"]
    assert token 