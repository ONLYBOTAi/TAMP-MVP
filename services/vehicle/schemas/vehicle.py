from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from models.vehicle import VehicleType

class VehicleBase(BaseModel):
    """Base schema for vehicle data."""
    make: str = Field(..., example="Toyota", description="Vehicle manufacturer", min_length=1, max_length=50)
    model: str = Field(..., example="Camry", description="Vehicle model name", min_length=1, max_length=50)
    year: int = Field(..., example=2023, description="Manufacturing year", ge=1900, le=2100)
    license_plate: str = Field(..., example="ABC123", description="Unique license plate number", min_length=1, max_length=20)
    vehicle_type: str = Field(..., example="car", description="Type of vehicle (car, truck, etc.)")
    color: Optional[str] = Field(None, example="Blue", description="Vehicle color", max_length=30)
    vin: Optional[str] = Field(None, example="1HGCM82633A123456", description="Vehicle Identification Number", min_length=17, max_length=17)

class VehicleCreate(VehicleBase):
    """Schema for creating a new vehicle."""
    pass

class VehicleUpdate(BaseModel):
    """Schema for updating a vehicle."""
    make: Optional[str] = Field(None, example="Honda", description="Vehicle manufacturer", min_length=1, max_length=50)
    model: Optional[str] = Field(None, example="Civic", description="Vehicle model name", min_length=1, max_length=50)
    year: Optional[int] = Field(None, example=2023, description="Manufacturing year", ge=1900, le=2100)
    license_plate: Optional[str] = Field(None, example="XYZ789", description="Unique license plate number", min_length=1, max_length=20)
    vehicle_type: Optional[str] = Field(None, example="car", description="Type of vehicle")
    color: Optional[str] = Field(None, example="Red", description="Vehicle color", max_length=30)
    vin: Optional[str] = Field(None, example="2HGES16575H123456", description="Vehicle Identification Number", min_length=17, max_length=17)

class VehicleInDB(VehicleBase):
    """Schema for vehicle data as stored in the database."""
    id: int = Field(..., example=1, description="Unique vehicle identifier")
    user_id: str = Field(..., example="user-123", description="ID of the vehicle owner")
    created_at: datetime = Field(..., example="2024-03-20T10:00:00Z", description="Vehicle creation timestamp")
    updated_at: datetime = Field(..., example="2024-03-20T10:00:00Z", description="Last update timestamp")

    class Config:
        from_attributes = True

class VehicleResponse(VehicleInDB):
    """Schema for vehicle data in API responses."""
    pass 