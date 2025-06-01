from fastapi import FastAPI, HTTPException, Depends, Header
from pydantic import BaseModel
from typing import List, Optional
import httpx
from datetime import datetime
import os
from sqlalchemy.orm import Session
from .database import get_db, engine, Base
from .models import Vehicle as VehicleModel
from fastapi.middleware.cors import CORSMiddleware
from routers import vehicle_routes
from fastapi.openapi.utils import get_openapi

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Vehicle Microservice",
    description="Manages vehicle data and operations for the TAMP platform",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(vehicle_routes.router)

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
@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "vehicle"}


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

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title="Vehicle Microservice API",
        version="1.0.0",
        description="""
        Vehicle management microservice for the TAMP platform.
        
        ## Features
        * Vehicle CRUD operations
        * JWT-based authentication
        * Role-based access control
        
        ## Authentication
        All endpoints require a valid JWT token in the Authorization header:
        ```
        Authorization: Bearer <your_token>
        ```
        """,
        routes=app.routes,
    )
    
    # Add security scheme
    openapi_schema["components"] = {
        "securitySchemes": {
            "bearerAuth": {
                "type": "http",
                "scheme": "bearer",
                "bearerFormat": "JWT",
            }
        }
    }
    
    # Add global security requirement
    openapi_schema["security"] = [{"bearerAuth": []}]
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi
