import pytest
from fastapi.testclient import TestClient
from datetime import datetime, timedelta

from tests.conftest import client
from tests.utils import create_test_token, create_expired_token

def test_valid_token_access(client: TestClient):
    """Test that a valid token allows access to protected endpoints."""
    token = create_test_token()
    headers = {"Authorization": f"Bearer {token}"}
    
    # Test GET endpoint
    response = client.get("/telemetry/data?vehicle_id=1", headers=headers)
    assert response.status_code == 200
    
    # Test POST endpoint
    data = {
        "vehicle_id": 1,
        "latitude": 37.7749,
        "longitude": -122.4194,
        "speed": 60.0
    }
    response = client.post("/telemetry/data", json=data, headers=headers)
    assert response.status_code == 201

def test_invalid_token_access(client: TestClient):
    """Test that an invalid token is rejected."""
    headers = {"Authorization": "Bearer invalid_token"}
    
    # Test GET endpoint
    response = client.get("/telemetry/data?vehicle_id=1", headers=headers)
    assert response.status_code == 401
    assert response.json()["detail"] == "Could not validate credentials"
    
    # Test POST endpoint
    data = {
        "vehicle_id": 1,
        "latitude": 37.7749,
        "longitude": -122.4194,
        "speed": 60.0
    }
    response = client.post("/telemetry/data", json=data, headers=headers)
    assert response.status_code == 401
    assert response.json()["detail"] == "Could not validate credentials"

def test_missing_token_access(client: TestClient):
    """Test that missing token is rejected."""
    # Test GET endpoint
    response = client.get("/telemetry/data?vehicle_id=1")
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"
    
    # Test POST endpoint
    data = {
        "vehicle_id": 1,
        "latitude": 37.7749,
        "longitude": -122.4194,
        "speed": 60.0
    }
    response = client.post("/telemetry/data", json=data)
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"

def test_expired_token_access(client: TestClient):
    """Test that an expired token is rejected."""
    token = create_expired_token()
    headers = {"Authorization": f"Bearer {token}"}
    
    # Test GET endpoint
    response = client.get("/telemetry/data?vehicle_id=1", headers=headers)
    assert response.status_code == 401
    assert response.json()["detail"] == "Could not validate credentials"
    
    # Test POST endpoint
    data = {
        "vehicle_id": 1,
        "latitude": 37.7749,
        "longitude": -122.4194,
        "speed": 60.0
    }
    response = client.post("/telemetry/data", json=data, headers=headers)
    assert response.status_code == 401
    assert response.json()["detail"] == "Could not validate credentials" 