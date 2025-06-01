import pytest
from fastapi import status
import requests
import time
import jwt
from datetime import datetime, timedelta

# Auth service URL (update this based on your setup)
AUTH_SERVICE_URL = "http://localhost:8001"

def test_auth_token_flow(client):
    """Test the complete auth token flow with vehicle operations."""
    # 1. Login to get token
    login_data = {
        "username": "test@example.com",
        "password": "testpassword"
    }
    
    try:
        auth_response = requests.post(f"{AUTH_SERVICE_URL}/auth/login", json=login_data)
        assert auth_response.status_code == status.HTTP_200_OK
        token = auth_response.json()["access_token"]
        
        # 2. Create vehicle with token
        vehicle_data = {
            "make": "Test Make",
            "model": "Test Model",
            "year": 2023,
            "license_plate": "TEST123",
            "vehicle_type": "car"
        }
        
        headers = {"Authorization": f"Bearer {token}"}
        create_response = client.post("/vehicles/", json=vehicle_data, headers=headers)
        assert create_response.status_code == status.HTTP_201_CREATED
        vehicle_id = create_response.json()["id"]
        
        # 3. Get vehicles with token
        get_response = client.get("/vehicles/", headers=headers)
        assert get_response.status_code == status.HTTP_200_OK
        assert len(get_response.json()) > 0
        
        # 4. Update vehicle with token
        update_data = {"make": "Updated Make"}
        update_response = client.put(f"/vehicles/{vehicle_id}", json=update_data, headers=headers)
        assert update_response.status_code == status.HTTP_200_OK
        assert update_response.json()["make"] == "Updated Make"
        
        # 5. Delete vehicle with token
        delete_response = client.delete(f"/vehicles/{vehicle_id}", headers=headers)
        assert delete_response.status_code == status.HTTP_204_NO_CONTENT
        
    except requests.exceptions.ConnectionError:
        pytest.skip("Auth service not available")

def test_invalid_token(client):
    """Test vehicle operations with invalid token."""
    headers = {"Authorization": "Bearer invalid_token"}
    
    # Try to get vehicles with invalid token
    response = client.get("/vehicles/", headers=headers)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

def test_expired_token(client):
    """Test vehicle operations with expired token."""
    # Create an expired token
    expired_token = jwt.encode(
        {
            "sub": "test-user-id",
            "exp": datetime.utcnow() - timedelta(hours=1)
        },
        "your-secret-key",
        algorithm="HS256"
    )
    
    headers = {"Authorization": f"Bearer {expired_token}"}
    
    # Try to get vehicles with expired token
    response = client.get("/vehicles/", headers=headers)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

def test_missing_token(client):
    """Test vehicle operations without token."""
    # Try to get vehicles without token
    response = client.get("/vehicles/")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED 