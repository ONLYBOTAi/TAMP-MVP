import pytest
from fastapi.testclient import TestClient

def test_register_user(client: TestClient):
    response = client.post(
        "/register",
        json={
            "email": "test@example.com",
            "password": "testpass123",
            "role": "user"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert data["email"] == "test@example.com"
    assert "password" not in data

def test_login_user(client: TestClient):
    # First register
    client.post(
        "/register",
        json={
            "email": "test@example.com",
            "password": "testpass123",
            "role": "user"
        }
    )
    
    # Then login
    response = client.post(
        "/login",
        data={
            "username": "test@example.com",
            "password": "testpass123"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_validate_token(client: TestClient):
    # Register and login
    client.post(
        "/register",
        json={
            "email": "test@example.com",
            "password": "testpass123",
            "role": "user"
        }
    )
    login_response = client.post(
        "/login",
        data={
            "username": "test@example.com",
            "password": "testpass123"
        }
    )
    token = login_response.json()["access_token"]
    
    # Validate token
    response = client.post(
        "/validate-token",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "sub" in data
    assert "role" in data 