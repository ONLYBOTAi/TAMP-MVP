import pytest
from fastapi.testclient import TestClient
from datetime import datetime, timedelta
from main import app
from services.auth.core.auth import create_access_token

client = TestClient(app)

# Test data
test_user = {
    "id": "1",
    "email": "test@example.com",
    "is_active": True
}

test_request = {
    "origin": {
        "latitude": 40.7128,
        "longitude": -74.0060,
        "address": "New York, NY"
    },
    "destination": {
        "latitude": 34.0522,
        "longitude": -118.2437,
        "address": "Los Angeles, CA"
    },
    "cargo_type": "general",
    "weight": 1000.0,
    "volume": 10.0,
    "pickup_time": (datetime.now() + timedelta(hours=1)).isoformat(),
    "delivery_deadline": (datetime.now() + timedelta(days=2)).isoformat(),
    "special_requirements": ["temperature_control"]
}

@pytest.fixture
def auth_headers():
    """Create authentication headers for testing"""
    access_token = create_access_token(test_user)
    return {"Authorization": f"Bearer {access_token}"}

def test_get_matches_unauthorized():
    """Test getting matches without authentication"""
    response = client.get("/api/v1/match", params=test_request)
    assert response.status_code == 401

def test_get_matches_authorized(auth_headers):
    """Test getting matches with authentication"""
    response = client.get("/api/v1/match", params=test_request, headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert "vehicle" in data[0]
    assert "match_score" in data[0]

def test_create_request_unauthorized():
    """Test creating request without authentication"""
    response = client.post("/api/v1/request", json=test_request)
    assert response.status_code == 401

def test_create_request_authorized(auth_headers):
    """Test creating request with authentication"""
    response = client.post("/api/v1/request", json=test_request, headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert "request_id" in data
    assert "status" in data
    assert "matches" in data
    assert "total_matches" in data

def test_invalid_request_format(auth_headers):
    """Test request with invalid format"""
    invalid_request = test_request.copy()
    invalid_request["weight"] = -1  # Invalid weight
    response = client.post("/api/v1/request", json=invalid_request, headers=auth_headers)
    assert response.status_code == 422 