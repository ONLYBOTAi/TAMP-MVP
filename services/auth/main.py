"""
FastAPI application entry point for the auth service.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import auth_routes
from models.base import Base  # Import shared Base
from models import user_model, vehicle_model  # Import models to register them
from db.db import engine

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

@app.get("/")
async def root():
    """Root endpoint to verify service is running."""
    return {"message": "Auth Service is running"}

# Let Alembic handle migrations — no manual table creation here.
