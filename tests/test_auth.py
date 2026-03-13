"""Tests for POST /auth/register and POST /auth/login."""


def test_register_success(client):
    resp = client.post(
        "/auth/register",
        json={
            "username": "alice",
            "email": "alice@example.com",
            "password": "secret123",
        },
    )
    assert resp.status_code == 201
    data = resp.json()
    assert data["username"] == "alice"
    assert data["email"] == "alice@example.com"
    assert "id" in data


def test_register_duplicate_username(client):
    payload = {
        "username": "bob",
        "email": "bob@example.com",
        "password": "pass123",
    }
    client.post("/auth/register", json=payload)
    resp = client.post("/auth/register", json=payload)
    assert resp.status_code == 409


def test_login_success(client):
    client.post(
        "/auth/register",
        json={
            "username": "charlie",
            "email": "charlie@example.com",
            "password": "pass123",
        },
    )
    resp = client.post(
        "/auth/login",
        json={"username": "charlie", "password": "pass123"},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_wrong_password(client):
    client.post(
        "/auth/register",
        json={
            "username": "dave",
            "email": "dave@example.com",
            "password": "correct",
        },
    )
    resp = client.post(
        "/auth/login",
        json={"username": "dave", "password": "wrong"},
    )
    assert resp.status_code == 401
