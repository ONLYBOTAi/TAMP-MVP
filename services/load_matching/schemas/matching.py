from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from services.vehicle.schemas import Vehicle

class Location(BaseModel):
    """Location coordinates"""
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
    address: Optional[str] = None

class MatchRequest(BaseModel):
    """Load matching request"""
    origin: Location
    destination: Location
    cargo_type: str
    weight: float = Field(..., gt=0)
    volume: float = Field(..., gt=0)
    pickup_time: datetime
    delivery_deadline: datetime
    special_requirements: Optional[List[str]] = None

class TruckMatch(BaseModel):
    """Matched truck details"""
    vehicle: Vehicle
    match_score: float = Field(..., ge=0, le=1)
    estimated_arrival: datetime
    distance: float  # in kilometers
    estimated_cost: float
    special_requirements_met: List[str]

class MatchResponse(BaseModel):
    """Match request response"""
    request_id: str
    status: str
    created_at: datetime
    matches: List[TruckMatch]
    total_matches: int 