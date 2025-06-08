from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from sqlalchemy.orm import Session
from typing import List
import logging
from datetime import datetime
from core.config import get_settings
from core.database import engine, Base, init_models
from contextlib import asynccontextmanager

from core.logging import setup_logging
from routers import telemetry_routes

# Setup logging
logger = setup_logging()

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_models()
    yield

# Initialize FastAPI app
app = FastAPI(
    title="Telematics Service",
    description="Service for handling vehicle telemetry data",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TODO: Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(telemetry_routes.router, prefix="/telemetry", tags=["telemetry"])

@app.on_event("startup")
async def startup_event():
    logger.info("Telematics service starting up")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Telematics service shutting down")

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

def custom_openapi():
    """Custom OpenAPI schema with JWT authentication."""
    if app.openapi_schema:
        return app.openapi_schema
        
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description="Telematics service API with JWT authentication",
        routes=app.routes,
    )
    
    # Add security scheme
    openapi_schema["components"] = {
        "securitySchemes": {
            "BearerAuth": {
                "type": "http",
                "scheme": "bearer",
                "bearerFormat": "JWT"
            }
        }
    }
    
    # Add global security requirement
    openapi_schema["security"] = [{"BearerAuth": []}]
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

@app.get("/")
async def root():
    """Root endpoint for health check."""
    return {
        "service": get_settings().PROJECT_NAME,
        "version": get_settings().VERSION,
        "status": "healthy"
    } 