import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.core.config import get_settings
from app.schemas.user import UserCreate
from app.models.user import Role

def test_create_user(client: TestClient, db_session: Session):
    settings = get_settings()
    response = client.post(
        f"{settings.API_V1_STR}/auth/register",
        json={"email": "test@example.com", "password": "testpassword", "name": "Test User", "role": "user"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"
    assert "id" in data
    assert "password_hash" not in data


def test_login(client: TestClient, db_session: Session):
    settings = get_settings()
    # First, create a user
    client.post(
        f"{settings.API_V1_STR}/auth/register",
        json={"email": "testlogin@example.com", "password": "testpassword", "name": "Test Login User", "role": "user"},
    )
    # Then, log in
    response = client.post(
        f"{settings.API_V1_STR}/auth/login",
        data={"username": "testlogin@example.com", "password": "testpassword"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def get_auth_headers(client: TestClient, email: str, password: str) -> dict:
    settings = get_settings()
    response = client.post(
        f"{settings.API_V1_STR}/auth/login",
        data={"username": email, "password": password},
    )
    data = response.json()
    access_token = data["access_token"]
    return {"Authorization": f"Bearer {access_token}"}


def test_read_user_me(client: TestClient, db_session: Session):
    settings = get_settings()
    email = "testme@example.com"
    password = "testpassword"
    client.post(
        f"{settings.API_V1_STR}/auth/register",
        json={"email": email, "password": password, "name": "Test Me User", "role": "user"},
    )
    headers = get_auth_headers(client, email, password)
    response = client.get(f"{settings.API_V1_STR}/auth/me", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == email


def test_update_user_me(client: TestClient, db_session: Session):
    settings = get_settings()
    email = "testupdate@example.com"
    password = "testpassword"
    client.post(
        f"{settings.API_V1_STR}/auth/register",
        json={"email": email, "password": password, "name": "Test Update User", "role": "user"},
    )
    headers = get_auth_headers(client, email, password)
    response = client.put(
        f"{settings.API_V1_STR}/auth/me",
        headers=headers,
        json={"name": "Updated Name"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Name"
    assert data["email"] == email
