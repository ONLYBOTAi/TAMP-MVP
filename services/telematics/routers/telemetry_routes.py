from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta

from core.database import get_db
from core.security import get_current_user
print("✅ get_current_user being used from:", get_current_user.__module__)

from models.telemetry import TelemetryData, TelemetryAlert
from schemas.telemetry import (
    TelemetryDataCreate,
    TelemetryData as TelemetryDataSchema,
    TelemetryAlertCreate,
    TelemetryAlert as TelemetryAlertSchema,
    TelemetryAlertUpdate
)

router = APIRouter(
    tags=["Telemetry"]
)

@router.post("/data", response_model=TelemetryDataSchema, status_code=201)
async def create_telemetry_data(
    data: TelemetryDataCreate,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user)
):
    """
    Create new telemetry data entry.
    
    - **vehicle_id**: ID of the vehicle
    - **latitude**: Vehicle's latitude
    - **longitude**: Vehicle's longitude
    - **altitude**: Vehicle's altitude (optional)
    - **speed**: Vehicle's speed in km/h (optional)
    - **engine_rpm**: Engine RPM (optional)
    - **fuel_level**: Fuel level percentage (optional)
    - **engine_temperature**: Engine temperature in Celsius (optional)
    - **battery_voltage**: Battery voltage (optional)
    - **odometer**: Total distance traveled in kilometers (optional)
    - **trip_distance**: Current trip distance in kilometers (optional)
    - **diagnostic_codes**: OBD diagnostic codes (optional)
    - **warning_lights**: Warning light statuses (optional)
    """
    db_telemetry = TelemetryData(**data.model_dump())
    db.add(db_telemetry)
    db.commit()
    db.refresh(db_telemetry)
    return db_telemetry

@router.get("/data", response_model=List[TelemetryDataSchema])
async def get_telemetry_data(
    vehicle_id: int,
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
    limit: int = Query(100, le=1000),
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user)
):
    """
    Get telemetry data for a vehicle within a time range.
    
    - **vehicle_id**: ID of the vehicle
    - **start_time**: Start of time range (optional)
    - **end_time**: End of time range (optional)
    - **limit**: Maximum number of records to return (max 1000)
    """
    query = db.query(TelemetryData).filter(TelemetryData.vehicle_id == vehicle_id)
    
    if start_time:
        query = query.filter(TelemetryData.timestamp >= start_time)
    if end_time:
        query = query.filter(TelemetryData.timestamp <= end_time)
    
    query = query.order_by(TelemetryData.timestamp.desc()).limit(limit)
    return query.all()

@router.post("/alerts", response_model=TelemetryAlertSchema, status_code=201)
async def create_telemetry_alert(
    alert: TelemetryAlertCreate,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user)
):
    """
    Create new telemetry alert.
    
    - **vehicle_id**: ID of the vehicle
    - **alert_type**: Type of alert (SPEED, ENGINE, BATTERY, etc.)
    - **severity**: Alert severity (INFO, WARNING, CRITICAL)
    - **message**: Alert message
    - **context_data**: Additional context data (optional)
    """
    db_alert = TelemetryAlert(**alert.model_dump())
    db.add(db_alert)
    db.commit()
    db.refresh(db_alert)
    return db_alert

@router.get("/alerts", response_model=List[TelemetryAlertSchema])
async def get_telemetry_alerts(
    vehicle_id: int,
    resolved: Optional[bool] = None,
    alert_type: Optional[str] = None,
    severity: Optional[str] = None,
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
    limit: int = Query(100, le=1000),
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user)
):
    """
    Get telemetry alerts for a vehicle with optional filters.
    
    - **vehicle_id**: ID of the vehicle
    - **resolved**: Filter by resolution status (optional)
    - **alert_type**: Filter by alert type (optional)
    - **severity**: Filter by severity (optional)
    - **start_time**: Start of time range (optional)
    - **end_time**: End of time range (optional)
    - **limit**: Maximum number of records to return (max 1000)
    """
    query = db.query(TelemetryAlert).filter(TelemetryAlert.vehicle_id == vehicle_id)
    
    if resolved is not None:
        query = query.filter(TelemetryAlert.resolved == resolved)
    if alert_type:
        query = query.filter(TelemetryAlert.alert_type == alert_type)
    if severity:
        query = query.filter(TelemetryAlert.severity == severity)
    if start_time:
        query = query.filter(TelemetryAlert.timestamp >= start_time)
    if end_time:
        query = query.filter(TelemetryAlert.timestamp <= end_time)
    
    return query.order_by(TelemetryAlert.timestamp.desc()).limit(limit).all()

@router.patch("/alerts/{alert_id}", response_model=TelemetryAlertSchema)
async def update_telemetry_alert(
    alert_id: int,
    alert_update: TelemetryAlertUpdate,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user)
):
    """
    Update telemetry alert status.
    
    - **alert_id**: ID of the alert to update
    - **resolved**: New resolution status
    - **resolved_at**: Timestamp of resolution (optional)
    """
    db_alert = db.query(TelemetryAlert).filter(TelemetryAlert.id == alert_id).first()
    if not db_alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    
    for field, value in alert_update.model_dump(exclude_unset=True).items():
        setattr(db_alert, field, value)
    
    db.commit()
    db.refresh(db_alert)
    return db_alert 