from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import matching_routes

app = FastAPI(
    title="Load Matching Service",
    description="Service for matching available trucks with load requests",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(matching_routes.router, prefix="/api/v1", tags=["matching"])

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"} 