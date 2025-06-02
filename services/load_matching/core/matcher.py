import httpx
import structlog
from typing import List, Optional
from datetime import datetime
from tenacity import retry, stop_after_attempt, wait_fixed
from schemas.matching import MatchRequest, MatchResponse, TruckMatch
from services.auth.schemas import User
from services.vehicle.schemas import Vehicle

logger = structlog.get_logger()

class LoadMatcher:
    def __init__(self):
        self.vehicle_service_url = "http://localhost:8002"  # Will be configurable
        self.timeout = 5.0
        self.client = httpx.AsyncClient(timeout=self.timeout)

    @retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
    async def _get_available_vehicles(self) -> List[Vehicle]:
        """Fetch available vehicles from vehicle service"""
        try:
            response = await self.client.get(f"{self.vehicle_service_url}/api/v1/vehicles/available")
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            logger.error("failed_to_fetch_vehicles", error=str(e))
            raise

    async def find_matches(self, request: MatchRequest) -> List[TruckMatch]:
        """
        Find matching trucks for a load request
        
        Args:
            request: The load matching request
            
        Returns:
            List of matching trucks with scores
        """
        try:
            # Get available vehicles
            vehicles = await self._get_available_vehicles()
            
            # TODO: Implement matching algorithm
            # For now, return mock matches
            matches = []
            for vehicle in vehicles[:3]:  # Mock: return first 3 vehicles
                match = TruckMatch(
                    vehicle=vehicle,
                    match_score=0.85,  # Mock score
                    estimated_arrival=datetime.now(),
                    distance=100.0,  # Mock distance
                    estimated_cost=500.0,  # Mock cost
                    special_requirements_met=["temperature_control", "hazmat"]
                )
                matches.append(match)
            
            return matches
            
        except Exception as e:
            logger.error("matching_failed", error=str(e))
            raise

    async def create_request(self, request: MatchRequest, user: User) -> MatchResponse:
        """
        Create a new match request
        
        Args:
            request: The match request details
            user: The user creating the request
            
        Returns:
            The created match request response
        """
        try:
            # Find matches
            matches = await self.find_matches(request)
            
            # Create response
            response = MatchResponse(
                request_id="REQ-001",  # TODO: Generate proper ID
                status="pending",
                created_at=datetime.now(),
                matches=matches,
                total_matches=len(matches)
            )
            
            return response
            
        except Exception as e:
            logger.error("request_creation_failed", error=str(e))
            raise

    async def close(self):
        """Close the HTTP client"""
        await self.client.aclose() 