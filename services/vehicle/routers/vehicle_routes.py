from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import logging

from ..database import get_db
from ..models.vehicle import Vehicle
from ..schemas.vehicle import VehicleCreate, VehicleResponse, VehicleUpdate
from ..core.security import get_current_user
from ..core.error_handlers import handle_db_error, handle_not_found, handle_auth_error

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/vehicles",
    tags=["vehicles"],
    responses={404: {"description": "Vehicle not found"}},
)

@router.post(
    "/",
    response_model=VehicleResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new vehicle",
    description="Create a new vehicle for the authenticated user. Requires valid JWT token.",
    response_description="The created vehicle"
)
async def create_vehicle(
    vehicle: VehicleCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Create a new vehicle with the following information:
    
    - **make**: Vehicle manufacturer
    - **model**: Vehicle model name
    - **year**: Manufacturing year
    - **license_plate**: Unique license plate number
    - **vehicle_type**: Type of vehicle (car, truck, etc.)
    - **color**: Optional vehicle color
    - **vin**: Optional Vehicle Identification Number
    """
    try:
        logger.info(f"Creating new vehicle for user {current_user['sub']}")
        db_vehicle = Vehicle(
            **vehicle.dict(),
            user_id=current_user["sub"]
        )
        db.add(db_vehicle)
        db.commit()
        db.refresh(db_vehicle)
        logger.info(f"Successfully created vehicle with ID {db_vehicle.id}")
        return db_vehicle
    except Exception as e:
        handle_db_error("create_vehicle", e)

@router.get(
    "/",
    response_model=List[VehicleResponse],
    summary="Get all vehicles",
    description="Retrieve all vehicles owned by the authenticated user. Requires valid JWT token."
)
async def get_vehicles(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Get all vehicles for the authenticated user.
    
    Returns a list of vehicles with their details:
    - Vehicle ID
    - Make and model
    - Year and license plate
    - Vehicle type and color
    - Creation and update timestamps
    """
    try:
        logger.info(f"Retrieving vehicles for user {current_user['sub']}")
        vehicles = db.query(Vehicle).filter(
            Vehicle.user_id == current_user["sub"]
        ).all()
        logger.info(f"Found {len(vehicles)} vehicles for user {current_user['sub']}")
        return vehicles
    except Exception as e:
        handle_db_error("get_vehicles", e)

@router.get(
    "/{vehicle_id}",
    response_model=VehicleResponse,
    summary="Get a specific vehicle",
    description="Retrieve details of a specific vehicle by ID. Requires valid JWT token."
)
async def get_vehicle(
    vehicle_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Get a specific vehicle by ID.
    
    Parameters:
    - **vehicle_id**: The ID of the vehicle to retrieve
    
    Returns:
    - Vehicle details if found
    - 404 error if vehicle not found or not owned by user
    """
    try:
        logger.info(f"Retrieving vehicle {vehicle_id} for user {current_user['sub']}")
        vehicle = db.query(Vehicle).filter(
            Vehicle.id == vehicle_id,
            Vehicle.user_id == current_user["sub"]
        ).first()
        
        if not vehicle:
            handle_not_found(vehicle_id)
            
        logger.info(f"Successfully retrieved vehicle {vehicle_id}")
        return vehicle
    except Exception as e:
        handle_db_error("get_vehicle", e)

@router.put(
    "/{vehicle_id}",
    response_model=VehicleResponse,
    summary="Update a vehicle",
    description="Update details of a specific vehicle. Requires valid JWT token."
)
async def update_vehicle(
    vehicle_id: int,
    vehicle_update: VehicleUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Update a specific vehicle.
    
    Parameters:
    - **vehicle_id**: The ID of the vehicle to update
    
    Request body:
    - **make**: Optional new make
    - **model**: Optional new model
    - **year**: Optional new year
    - **license_plate**: Optional new license plate
    - **vehicle_type**: Optional new vehicle type
    - **color**: Optional new color
    - **vin**: Optional new VIN
    
    Returns:
    - Updated vehicle details
    - 404 error if vehicle not found or not owned by user
    """
    try:
        logger.info(f"Updating vehicle {vehicle_id} for user {current_user['sub']}")
        db_vehicle = db.query(Vehicle).filter(
            Vehicle.id == vehicle_id,
            Vehicle.user_id == current_user["sub"]
        ).first()
        
        if not db_vehicle:
            handle_not_found(vehicle_id)
        
        update_data = vehicle_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_vehicle, field, value)
        
        db.commit()
        db.refresh(db_vehicle)
        logger.info(f"Successfully updated vehicle {vehicle_id}")
        return db_vehicle
    except Exception as e:
        handle_db_error("update_vehicle", e)

@router.delete(
    "/{vehicle_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a vehicle",
    description="Delete a specific vehicle. Requires valid JWT token."
)
async def delete_vehicle(
    vehicle_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Delete a specific vehicle.
    
    Parameters:
    - **vehicle_id**: The ID of the vehicle to delete
    
    Returns:
    - 204 No Content on successful deletion
    - 404 error if vehicle not found or not owned by user
    """
    try:
        logger.info(f"Deleting vehicle {vehicle_id} for user {current_user['sub']}")
        db_vehicle = db.query(Vehicle).filter(
            Vehicle.id == vehicle_id,
            Vehicle.user_id == current_user["sub"]
        ).first()
        
        if not db_vehicle:
            handle_not_found(vehicle_id)
        
        db.delete(db_vehicle)
        db.commit()
        logger.info(f"Successfully deleted vehicle {vehicle_id}")
        return None
    except Exception as e:
        handle_db_error("delete_vehicle", e) 