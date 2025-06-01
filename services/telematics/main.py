from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from core.config import get_settings
from core.database import engine, Base

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title=get_settings().PROJECT_NAME,
    version=get_settings().VERSION,
    openapi_url=f"{get_settings().API_V1_STR}/openapi.json"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import and include routers
from routers import telemetry_routes
app.include_router(
    telemetry_routes.router,
    prefix=f"{get_settings().API_V1_STR}/telemetry",
    tags=["telemetry"]
)

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