"""Tests for /lists/{task_list_id}/tasks/ endpoints."""


# ── GET /lists/{id}/tasks/ ────────────────────────────────────────────────────


def test_get_all_tasks_success(client, auth_headers, task_list_id):
    resp = client.get(
        f"/lists/{task_list_id}/tasks/", headers=auth_headers
    )
    assert resp.status_code == 200
    data = resp.json()
    assert "tasks" in data
    assert isinstance(data["tasks"], list)


def test_get_all_tasks_no_token(client, auth_headers, task_list_id):
    resp = client.get(f"/lists/{task_list_id}/tasks/")
    assert resp.status_code == 401


# ── POST /lists/{id}/tasks/ ───────────────────────────────────────────────────


def test_create_task_success(client, auth_headers, task_list_id):
    resp = client.post(
        f"/lists/{task_list_id}/tasks/",
        json={"title": "New Task", "description": "Task description"},
        headers=auth_headers,
    )
    assert resp.status_code == 201
    data = resp.json()
    assert data["title"] == "New Task"
    assert data["status"] == "pending"
    assert "id" in data


def test_create_task_no_token(client, auth_headers, task_list_id):
    resp = client.post(
        f"/lists/{task_list_id}/tasks/",
        json={"title": "No auth"},
    )
    assert resp.status_code == 401


# ── GET /lists/{id}/tasks/{task_id} ──────────────────────────────────────────


def test_get_task_by_id_success(client, auth_headers, task_list_id, task_id):
    resp = client.get(
        f"/lists/{task_list_id}/tasks/{task_id}", headers=auth_headers
    )
    assert resp.status_code == 200
    assert resp.json()["id"] == task_id


def test_get_task_by_id_not_found(client, auth_headers, task_list_id):
    resp = client.get(
        f"/lists/{task_list_id}/tasks/9999", headers=auth_headers
    )
    assert resp.status_code == 404


# ── PUT /lists/{id}/tasks/{task_id} ──────────────────────────────────────────


def test_update_task_success(client, auth_headers, task_list_id, task_id):
    resp = client.put(
        f"/lists/{task_list_id}/tasks/{task_id}",
        json={"title": "Updated Task", "priority": "high"},
        headers=auth_headers,
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["title"] == "Updated Task"
    assert data["priority"] == "high"


def test_update_task_no_token(client, auth_headers, task_list_id, task_id):
    resp = client.put(
        f"/lists/{task_list_id}/tasks/{task_id}",
        json={"title": "No auth"},
    )
    assert resp.status_code == 401


# ── PATCH /lists/{id}/tasks/{task_id}/status ─────────────────────────────────


def test_change_status_success(client, auth_headers, task_list_id, task_id):
    resp = client.patch(
        f"/lists/{task_list_id}/tasks/{task_id}/status",
        json={"status": "in_progress"},
        headers=auth_headers,
    )
    assert resp.status_code == 200
    assert resp.json()["status"] == "in_progress"


def test_change_status_not_found(client, auth_headers, task_list_id):
    resp = client.patch(
        f"/lists/{task_list_id}/tasks/9999/status",
        json={"status": "done"},
        headers=auth_headers,
    )
    assert resp.status_code == 404


# ── DELETE /lists/{id}/tasks/{task_id} ───────────────────────────────────────


def test_delete_task_success(client, auth_headers, task_list_id, task_id):
    resp = client.delete(
        f"/lists/{task_list_id}/tasks/{task_id}", headers=auth_headers
    )
    assert resp.status_code == 204


def test_delete_task_not_found(client, auth_headers, task_list_id):
    resp = client.delete(
        f"/lists/{task_list_id}/tasks/9999", headers=auth_headers
    )
    assert resp.status_code == 404
