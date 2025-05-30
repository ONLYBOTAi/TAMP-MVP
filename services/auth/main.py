"""
FastAPI application entry point for the auth service.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from services.auth.routers import auth_routes
from services.auth.models.base import Base  # Import shared Base
from services.auth.models import user_model, vehicle_model  # Import models to register them
from services.auth.db.db import engine

app = FastAPI(title="Auth Service")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_routes.router)

@app.on_event("startup")
async def startup():
    """Create database tables on startup."""
    async with engine.begin() as conn:
        # Create tables one at a time in the correct order
        # First create the users table
        await conn.run_sync(lambda sync_conn: Base.metadata.tables['users'].create(sync_conn))
        # Then create the vehicles table
        await conn.run_sync(lambda sync_conn: Base.metadata.tables['vehicles'].create(sync_conn))

@app.get("/")
async def root():
    """Root endpoint to verify service is running."""
    return {"message": "Auth Service is running"}
