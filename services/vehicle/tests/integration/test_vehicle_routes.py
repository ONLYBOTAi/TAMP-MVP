import pytest
from fastapi import status
from ..conftest import MOCK_USER

def test_create_vehicle(client):
    """Test creating a new vehicle."""
    vehicle_data = {
        "make": "Honda",
        "model": "Civic",
        "year": 2021,
        "license_plate": "XYZ789",
        "vehicle_type": "car",
        "color": "Blue"
    }
    
    response = client.post("/vehicles/", json=vehicle_data)
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["make"] == vehicle_data["make"]
    assert data["model"] == vehicle_data["model"]
    assert data["user_id"] == MOCK_USER["sub"]

def test_get_vehicles(client, test_vehicle):
    """Test getting all vehicles for a user."""
    response = client.get("/vehicles/")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 1
    assert data[0]["id"] == test_vehicle.id
    assert data[0]["make"] == test_vehicle.make

def test_get_vehicle(client, test_vehicle):
    """Test getting a specific vehicle."""
    response = client.get(f"/vehicles/{test_vehicle.id}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == test_vehicle.id
    assert data["make"] == test_vehicle.make

def test_get_nonexistent_vehicle(client):
    """Test getting a vehicle that doesn't exist."""
    response = client.get("/vehicles/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_update_vehicle(client, test_vehicle):
    """Test updating a vehicle."""
    update_data = {
        "make": "Updated Make",
        "model": "Updated Model"
    }
    
    response = client.put(f"/vehicles/{test_vehicle.id}", json=update_data)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["make"] == update_data["make"]
    assert data["model"] == update_data["model"]

def test_update_nonexistent_vehicle(client):
    """Test updating a vehicle that doesn't exist."""
    update_data = {"make": "Updated Make"}
    response = client.put("/vehicles/999", json=update_data)
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_delete_vehicle(client, test_vehicle):
    """Test deleting a vehicle."""
    response = client.delete(f"/vehicles/{test_vehicle.id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    
    # Verify vehicle is deleted
    get_response = client.get(f"/vehicles/{test_vehicle.id}")
    assert get_response.status_code == status.HTTP_404_NOT_FOUND

def test_delete_nonexistent_vehicle(client):
    """Test deleting a vehicle that doesn't exist."""
    response = client.delete("/vehicles/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND 