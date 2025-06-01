from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from models.vehicle import VehicleType

class VehicleBase(BaseModel):
    """Base schema for vehicle data."""
    make: str = Field(..., min_length=1, max_length=50)
    model: str = Field(..., min_length=1, max_length=50)
    year: int = Field(..., ge=1900, le=datetime.now().year + 1)
    license_plate: str = Field(..., min_length=1, max_length=20)
    vehicle_type: VehicleType
    color: Optional[str] = Field(None, max_length=30)
    vin: Optional[str] = Field(None, min_length=17, max_length=17)

class VehicleCreate(VehicleBase):
    """Schema for creating a new vehicle."""
    pass

class VehicleUpdate(BaseModel):
    """Schema for updating a vehicle."""
    make: Optional[str] = Field(None, min_length=1, max_length=50)
    model: Optional[str] = Field(None, min_length=1, max_length=50)
    year: Optional[int] = Field(None, ge=1900, le=datetime.now().year + 1)
    license_plate: Optional[str] = Field(None, min_length=1, max_length=20)
    vehicle_type: Optional[VehicleType] = None
    color: Optional[str] = Field(None, max_length=30)
    vin: Optional[str] = Field(None, min_length=17, max_length=17)

class VehicleInDB(VehicleBase):
    """Schema for vehicle data as stored in the database."""
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class VehicleResponse(VehicleInDB):
    """Schema for vehicle data in API responses."""
    pass 