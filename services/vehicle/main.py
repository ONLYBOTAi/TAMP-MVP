from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
import httpx
from datetime import datetime
import os

app = FastAPI(title="Vehicle Service")

# Models
class Vehicle(BaseModel):
    make: str
    model: str
    year: int
    license_plate: str

class VehicleResponse(Vehicle):
    id: int
    owner_id: str
    created_at: datetime

# Dependencies
async def verify_token(token: str):
    auth_service_url = os.getenv("AUTH_SERVICE_URL", "http://tamp_auth_svc:8000")
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{auth_service_url}/validate-token",
                params={"token": token}
            )
            if response.status_code == 200:
                return response.json()
            raise HTTPException(status_code=401, detail="Invalid token")
        except Exception as e:
            raise HTTPException(status_code=401, detail="Authentication failed")

# Routes
@app.get("/")
async def root():
    return {"message": "Vehicle Service is running"}

@app.post("/vehicles", response_model=VehicleResponse)
async def create_vehicle(vehicle: Vehicle, token: str):
    user = await verify_token(token)
    if user["role"] != "truck_owner":
        raise HTTPException(status_code=403, detail="Only truck owners can create vehicles")
    
    # Here you would typically save to a database
    # For now, we'll return a mock response
    return {
        **vehicle.dict(),
        "id": 1,
        "owner_id": user.get("sub"),
        "created_at": datetime.now()
    }

@app.get("/vehicles", response_model=List[VehicleResponse])
async def get_vehicles(token: str):
    await verify_token(token)
    # Here you would typically fetch from a database
    # For now, we'll return a mock response
    return []
