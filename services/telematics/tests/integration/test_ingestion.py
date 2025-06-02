import pytest
from fastapi.testclient import TestClient
from datetime import datetime
from unittest.mock import AsyncMock, patch

from main import app
from core.security import create_access_token
from schemas.telemetry import TelemetryDataCreate

client = TestClient(app)

@pytest.fixture
def valid_token():
    """Create a valid JWT token for testing."""
    return create_access_token({"sub": "testuser"})

@pytest.fixture
def invalid_token():
    """Create an invalid JWT token for testing."""
    return "invalid.token.here"

@pytest.fixture
def valid_telemetry_data():
    """Create valid telemetry data for testing."""
    return {
        "vehicle_id": 1,
        "latitude": 37.7749,
        "longitude": -122.4194,
        "altitude": 100.0,
        "speed": 60.0,
        "engine_rpm": 2500,
        "fuel_level": 75.5,
        "engine_temperature": 90.0,
        "battery_voltage": 12.6,
        "odometer": 50000.0,
        "trip_distance": 25.0,
        "diagnostic_codes": {"P0300": "Random/Multiple Cylinder Misfire"},
        "warning_lights": {"check_engine": True},
        "timestamp": datetime.utcnow().isoformat()
    }

@pytest.fixture
def auth_headers(valid_token):
    """Create authorization headers with valid token."""
    return {"Authorization": f"Bearer {valid_token}"}

@pytest.mark.asyncio
async def test_ingest_telemetry_success(valid_token, valid_telemetry_data):
    """Test successful telemetry ingestion."""
    with patch("core.vehicle_client.VehicleClient.get_vehicle") as mock_get_vehicle:
        mock_get_vehicle.return_value = {"id": 1, "status": "active"}
        
        response = client.post(
            "/telemetry/ingest",
            json=valid_telemetry_data,
            headers={"Authorization": f"Bearer {valid_token}"}
        )
        
        assert response.status_code == 202
        data = response.json()
        assert data["status"] == "queued"
        assert data["vehicle_id"] == valid_telemetry_data["vehicle_id"]
        assert "timestamp" in data
        assert "message" in data

@pytest.mark.asyncio
async def test_ingest_telemetry_unauthorized(invalid_token, valid_telemetry_data):
    """Test telemetry ingestion with invalid token."""
    response = client.post(
        "/telemetry/ingest",
        json=valid_telemetry_data,
        headers={"Authorization": f"Bearer {invalid_token}"}
    )
    
    assert response.status_code == 401
    assert "detail" in response.json()

@pytest.mark.asyncio
async def test_ingest_telemetry_vehicle_not_found(valid_token, valid_telemetry_data):
    """Test telemetry ingestion with non-existent vehicle."""
    with patch("core.vehicle_client.VehicleClient.get_vehicle") as mock_get_vehicle:
        mock_get_vehicle.return_value = None
        
        response = client.post(
            "/telemetry/ingest",
            json=valid_telemetry_data,
            headers={"Authorization": f"Bearer {valid_token}"}
        )
        
        assert response.status_code == 404
        assert response.json()["detail"] == "Vehicle not found"

@pytest.mark.asyncio
async def test_ingest_telemetry_invalid_data(valid_token):
    """Test telemetry ingestion with invalid data."""
    invalid_data = {
        "vehicle_id": "not_an_integer",  # Should be integer
        "latitude": "invalid",  # Should be float
        "longitude": -122.4194
    }
    
    response = client.post(
        "/telemetry/ingest",
        json=invalid_data,
        headers={"Authorization": f"Bearer {valid_token}"}
    )
    
    assert response.status_code == 422
    assert "detail" in response.json()

@pytest.mark.asyncio
async def test_ingest_telemetry_missing_required_fields(valid_token):
    """Test telemetry ingestion with missing required fields."""
    incomplete_data = {
        "vehicle_id": 1
        # Missing required latitude and longitude
    }
    
    response = client.post(
        "/telemetry/ingest",
        json=incomplete_data,
        headers={"Authorization": f"Bearer {valid_token}"}
    )
    
    assert response.status_code == 422
    assert "detail" in response.json()

def test_get_telemetry_status(auth_headers):
    """Test telemetry status endpoint."""
    vehicle_id = "test_vehicle_1"
    
    response = client.get(
        f"/telemetry/status/{vehicle_id}",
        headers=auth_headers
    )
    
    assert response.status_code == 200
    assert response.json()["vehicle_id"] == vehicle_id
    assert "status" in response.json()
    assert "last_update" in response.json()

def test_ingest_telemetry_invalid_data(auth_headers):
    """Test telemetry ingestion with invalid data."""
    invalid_data = {
        "vehicle_id": "test_vehicle_1",
        "timestamp": "invalid_timestamp",
        "data": {}
    }
    
    response = client.post(
        "/telemetry/ingest",
        headers=auth_headers,
        json=invalid_data
    )
    
    assert response.status_code == 422  # Validation error

def test_ingest_telemetry_unauthorized():
    """Test telemetry ingestion without authentication."""
    test_data = {
        "vehicle_id": "test_vehicle_1",
        "timestamp": datetime.utcnow().isoformat(),
        "data": {"speed": 60}
    }
    
    response = client.post(
        "/telemetry/ingest",
        json=test_data
    )
    
    assert response.status_code == 401  # Unauthorized 