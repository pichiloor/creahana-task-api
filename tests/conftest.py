import os

# Set env vars before importing any project module.
# This makes pydantic-settings use SQLite instead of PostgreSQL.
os.environ["DATABASE_URL"] = "sqlite:///./test_crehana.db"
os.environ["SECRET_KEY"] = "test-secret-key-for-testing-only"

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from api.main import app
from infrastructure.database import Base, get_db

TEST_DATABASE_URL = "sqlite:///./test_crehana.db"

# SQLite needs check_same_thread=False to work with FastAPI's TestClient.
test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
)
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=test_engine
)


def override_get_db():
    # Replaces the real database session with a test session.
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


# Replace the real get_db dependency with the test one for all requests.
app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(autouse=True)
def reset_db():
    # Create tables before each test and drop them after.
    # This ensures every test starts with a clean database.
    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def auth_headers(client):
    # Register a user and return the auth headers with a valid token.
    client.post(
        "/auth/register",
        json={
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "testpass123",
        },
    )
    resp = client.post(
        "/auth/login",
        json={"username": "testuser", "password": "testpass123"},
    )
    token = resp.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def task_list_id(client, auth_headers):
    # Create a task list and return its ID.
    resp = client.post(
        "/lists/",
        json={"title": "Fixture List", "description": "Created by fixture"},
        headers=auth_headers,
    )
    return resp.json()["id"]


@pytest.fixture
def task_id(client, auth_headers, task_list_id):
    # Create a task inside the fixture list and return its ID.
    resp = client.post(
        f"/lists/{task_list_id}/tasks/",
        json={"title": "Fixture Task", "description": "Created by fixture"},
        headers=auth_headers,
    )
    return resp.json()["id"]
