from fastapi import APIRouter, Depends, HTTPException, Query, BackgroundTasks, status
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
import logging

from core.database import get_db
from core.security import get_current_user
from core.vehicle_client import VehicleClient
from workers.ingestion_worker import process_telemetry_data
from models.telemetry import TelemetryData, TelemetryAlert
from schemas.telemetry import (
    TelemetryDataCreate,
    TelemetryData as TelemetryDataSchema,
    TelemetryAlertCreate,
    TelemetryAlert as TelemetryAlertSchema,
    TelemetryAlertUpdate
)

print("✅ get_current_user being used from:", get_current_user.__module__)

router = APIRouter(
    tags=["Telemetry"]
)

logger = logging.getLogger(__name__)

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

@router.post(
    "/ingest",
    response_model=Dict[str, Any],
    status_code=status.HTTP_202_ACCEPTED,
    summary="Ingest telemetry data from vehicles",
    description="""
    Accepts telemetry data from vehicles and queues it for asynchronous processing.
    
    The endpoint performs the following:
    1. Validates the vehicle exists in the system
    2. Queues the telemetry data for background processing
    3. Returns an immediate acknowledgment
    
    **Note**: This is an asynchronous endpoint. The actual processing happens in the background.
    """,
    responses={
        202: {
            "description": "Telemetry data accepted for processing",
            "content": {
                "application/json": {
                    "example": {
                        "message": "Telemetry data queued for processing",
                        "vehicle_id": "123",
                        "timestamp": "2024-03-14T12:00:00Z",
                        "status": "queued"
                    }
                }
            }
        },
        404: {
            "description": "Vehicle not found",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Vehicle not found"
                    }
                }
            }
        },
        422: {
            "description": "Validation error",
            "content": {
                "application/json": {
                    "example": {
                        "detail": [
                            {
                                "loc": ["body", "vehicle_id"],
                                "msg": "field required",
                                "type": "value_error.missing"
                            }
                        ]
                    }
                }
            }
        }
    }
)
async def ingest_telemetry(
    data: TelemetryDataCreate,
    background_tasks: BackgroundTasks,
    current_user: str = Depends(get_current_user),
    vehicle_client: VehicleClient = Depends()
):
    """
    Ingest telemetry data from vehicles.
    
    Args:
        data (TelemetryDataCreate): The telemetry data to ingest
        background_tasks (BackgroundTasks): FastAPI background tasks handler
        current_user (str): The authenticated user
        vehicle_client (VehicleClient): Vehicle service client
    
    Returns:
        Dict[str, Any]: Processing status and metadata
    
    Raises:
        HTTPException: If vehicle not found or validation fails
    """
    try:
        # Validate vehicle exists
        vehicle = await vehicle_client.get_vehicle(data.vehicle_id)
        if not vehicle:
            logger.warning(
                "Vehicle not found",
                extra={
                    "vehicle_id": data.vehicle_id,
                    "user": current_user
                }
            )
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Vehicle not found"
            )

        # Queue data for processing
        background_tasks.add_task(process_telemetry_data, data)
        
        logger.info(
            "Telemetry data queued for processing",
            extra={
                "vehicle_id": data.vehicle_id,
                "timestamp": datetime.utcnow().isoformat(),
                "user": current_user
            }
        )
        
        return {
            "message": "Telemetry data queued for processing",
            "vehicle_id": data.vehicle_id,
            "timestamp": datetime.utcnow().isoformat(),
            "status": "queued"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            "Error processing telemetry data",
            extra={
                "vehicle_id": data.vehicle_id,
                "error": str(e),
                "user": current_user
            }
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error processing telemetry data"
        )

@router.get("/status/{vehicle_id}", response_model=Dict[str, Any])
async def get_telemetry_status(
    vehicle_id: str,
    current_user: str = Depends(get_current_user)
):
    """
    Get telemetry status for a vehicle.
    
    Args:
        vehicle_id: ID of the vehicle
        current_user: The authenticated user
    
    Returns:
        Dict[str, Any]: Status information
    """
    try:
        return {
            "vehicle_id": vehicle_id,
            "status": "active",
            "last_update": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(
            "Failed to get telemetry status",
            extra={
                "vehicle_id": vehicle_id,
                "error": str(e),
                "user": current_user
            }
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get telemetry status"
        ) 