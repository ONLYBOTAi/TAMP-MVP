import httpx
from typing import Optional, Dict, Any
from fastapi import HTTPException, status
import structlog
from tenacity import retry, stop_after_attempt, wait_exponential

logger = structlog.get_logger(__name__)

class VehicleClient:
    """
    Client for interacting with the vehicle service.
    Handles fetching vehicle metadata and validation.
    """
    def __init__(self, base_url: str = "http://vehicle-service:8000"):
        self.base_url = base_url
        self.client = httpx.AsyncClient(
            base_url=base_url,
            timeout=5.0,
            follow_redirects=True
        )

    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.client.aclose()

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        reraise=True
    )
    async def get_vehicle(self, vehicle_id: int) -> Optional[Dict[str, Any]]:
        """
        Get vehicle information from the vehicle service.
        
        Args:
            vehicle_id (int): The ID of the vehicle to retrieve
            
        Returns:
            Optional[Dict[str, Any]]: Vehicle information if found, None otherwise
            
        Raises:
            HTTPException: If the vehicle service is unavailable
        """
        try:
            logger.info(
                "Fetching vehicle information",
                vehicle_id=vehicle_id,
                service_url=f"{self.base_url}/api/v1/vehicles/{vehicle_id}"
            )
            
            response = await self.client.get(f"/api/v1/vehicles/{vehicle_id}")
            
            if response.status_code == 404:
                logger.warning(
                    "Vehicle not found",
                    vehicle_id=vehicle_id,
                    status_code=response.status_code
                )
                return None
                
            response.raise_for_status()
            
            vehicle_data = response.json()
            logger.info(
                "Successfully retrieved vehicle information",
                vehicle_id=vehicle_id,
                status=vehicle_data.get("status")
            )
            
            return vehicle_data
            
        except httpx.TimeoutException:
            logger.error(
                "Timeout while fetching vehicle information",
                vehicle_id=vehicle_id,
                service_url=self.base_url
            )
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Vehicle service timeout"
            )
            
        except httpx.HTTPError as e:
            logger.error(
                "Error fetching vehicle information",
                vehicle_id=vehicle_id,
                error=str(e),
                status_code=getattr(e.response, "status_code", None)
            )
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Vehicle service unavailable"
            )

    async def validate_vehicle(self, vehicle_id: str) -> bool:
        """
        Validate that a vehicle exists and is active.
        """
        vehicle = await self.get_vehicle(vehicle_id)
        if not vehicle:
            return False
            
        # TODO: Add additional validation logic
        # For example, check if vehicle is active, has required sensors, etc.
        
        return True

async def get_vehicle_client() -> VehicleClient:
    """
    Dependency for getting a VehicleClient instance.
    """
    return VehicleClient() 