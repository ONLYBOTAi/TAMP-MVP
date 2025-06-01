from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime

class TelemetryDataBase(BaseModel):
    """Base schema for telemetry data."""
    vehicle_id: int
    latitude: float
    longitude: float
    altitude: Optional[float] = None
    speed: Optional[float] = None
    engine_rpm: Optional[int] = None
    fuel_level: Optional[float] = None
    engine_temperature: Optional[float] = None
    battery_voltage: Optional[float] = None
    odometer: Optional[float] = None
    trip_distance: Optional[float] = None
    diagnostic_codes: Optional[Dict[str, Any]] = None
    warning_lights: Optional[Dict[str, Any]] = None

class TelemetryDataCreate(TelemetryDataBase):
    """Schema for creating telemetry data."""
    pass

class TelemetryData(TelemetryDataBase):
    """Schema for telemetry data response."""
    id: int
    timestamp: datetime
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class TelemetryAlertBase(BaseModel):
    """Base schema for telemetry alerts."""
    vehicle_id: int
    alert_type: str = Field(..., description="Type of alert (e.g., SPEED, ENGINE, BATTERY)")
    severity: str = Field(..., description="Alert severity (INFO, WARNING, CRITICAL)")
    message: str
    context_data: Optional[Dict[str, Any]] = None

class TelemetryAlertCreate(TelemetryAlertBase):
    """Schema for creating telemetry alerts."""
    pass

class TelemetryAlert(TelemetryAlertBase):
    """Schema for telemetry alert response."""
    id: int
    timestamp: datetime
    resolved: bool
    resolved_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class TelemetryAlertUpdate(BaseModel):
    """Schema for updating telemetry alerts."""
    resolved: bool
    resolved_at: Optional[datetime] = None 