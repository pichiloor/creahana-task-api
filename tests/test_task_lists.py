"""Tests for /lists/ endpoints."""


# ── GET /lists/ ───────────────────────────────────────────────────────────────


def test_get_all_lists_success(client, auth_headers):
    resp = client.get("/lists/", headers=auth_headers)
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)


def test_get_all_lists_no_token(client):
    resp = client.get("/lists/")
    assert resp.status_code == 401


# ── POST /lists/ ──────────────────────────────────────────────────────────────


def test_create_list_success(client, auth_headers):
    resp = client.post(
        "/lists/",
        json={"title": "My New List", "description": "Some description"},
        headers=auth_headers,
    )
    assert resp.status_code == 201
    data = resp.json()
    assert data["title"] == "My New List"
    assert "id" in data


def test_create_list_no_token(client):
    resp = client.post("/lists/", json={"title": "No auth"})
    assert resp.status_code == 401


# ── GET /lists/{id} ───────────────────────────────────────────────────────────


def test_get_list_by_id_success(client, auth_headers, task_list_id):
    resp = client.get(f"/lists/{task_list_id}", headers=auth_headers)
    assert resp.status_code == 200
    assert resp.json()["id"] == task_list_id


def test_get_list_by_id_not_found(client, auth_headers):
    resp = client.get("/lists/9999", headers=auth_headers)
    assert resp.status_code == 404


# ── PUT /lists/{id} ───────────────────────────────────────────────────────────


def test_update_list_success(client, auth_headers, task_list_id):
    resp = client.put(
        f"/lists/{task_list_id}",
        json={"title": "Updated Title", "description": "Updated desc"},
        headers=auth_headers,
    )
    assert resp.status_code == 200
    assert resp.json()["title"] == "Updated Title"


def test_update_list_no_token(client, auth_headers, task_list_id):
    resp = client.put(
        f"/lists/{task_list_id}",
        json={"title": "No auth"},
    )
    assert resp.status_code == 401


# ── DELETE /lists/{id} ────────────────────────────────────────────────────────


def test_delete_list_success(client, auth_headers, task_list_id):
    resp = client.delete(f"/lists/{task_list_id}", headers=auth_headers)
    assert resp.status_code == 204


def test_delete_list_not_found(client, auth_headers):
    resp = client.delete("/lists/9999", headers=auth_headers)
    assert resp.status_code == 404
