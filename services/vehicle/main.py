from fastapi import FastAPI, HTTPException, Depends, Header
from pydantic import BaseModel
from typing import List, Optional
import httpx
from datetime import datetime
import os
from sqlalchemy.orm import Session
from .database import get_db
from .models import Vehicle as VehicleModel


app = FastAPI(title="Vehicle Service")


# Models
class VehicleBase(BaseModel):
    make: str
    model: str
    year: int
    license_plate: str

    class Config:
        from_attributes = True


class VehicleCreate(VehicleBase):
    pass


class VehicleResponse(VehicleBase):
    id: int
    owner_id: str
    created_at: datetime
    deleted_at: Optional[datetime] = None


# Dependencies
async def verify_token(authorization: str = Header(...)):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization header")
    
    token = authorization.split(" ")[1]
    auth_service_url = os.getenv(
        "AUTH_SERVICE_URL",
        "http://localhost:8000"
    )
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{auth_service_url}/validate-token",
                params={"token": token}
            )
            if response.status_code == 200:
                return response.json()
            raise HTTPException(status_code=401, detail="Invalid token")
        except Exception:
            raise HTTPException(
                status_code=401,
                detail="Authentication failed"
            )


# Routes
@app.get("/")
async def root():
    return {"message": "Vehicle Service is running"}


@app.post("/vehicles", response_model=VehicleResponse)
async def create_vehicle(
    vehicle: VehicleCreate,
    db: Session = Depends(get_db),
    user: dict = Depends(verify_token)
):
    if user["role"] != "truck_owner":
        raise HTTPException(
            status_code=403,
            detail="Only truck owners can create vehicles"
        )
    
    # Check if license plate already exists
    existing = db.query(VehicleModel).filter(
        VehicleModel.license_plate == vehicle.license_plate,
        VehicleModel.deleted_at.is_(None)
    ).first()
    
    if existing:
        raise HTTPException(
            status_code=400,
            detail="Vehicle with this license plate already exists"
        )
    
    # Create new vehicle
    db_vehicle = VehicleModel(
        **vehicle.dict(),
        owner_id=user["sub"],
        created_at=datetime.now()
    )
    
    db.add(db_vehicle)
    db.commit()
    db.refresh(db_vehicle)
    
    return db_vehicle


@app.get("/vehicles", response_model=List[VehicleResponse])
async def get_vehicles(
    db: Session = Depends(get_db),
    user: dict = Depends(verify_token)
):
    # For now, return all vehicles
    # TODO: Add filtering based on user role and ownership
    vehicles = db.query(VehicleModel).filter(
        VehicleModel.deleted_at.is_(None)
    ).all()
    
    return vehicles
