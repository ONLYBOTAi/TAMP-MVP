from fastapi import APIRouter, Depends, HTTPException, status, Request
from typing import List
import logging

from schemas.matcher_schema import MatchRequest, MatchResponse
from engine.matcher_logic import match_load_to_vehicle
# WARNING: The following import will fail unless core/security.py exists in matcher service
from core.security import JWTBearer, get_current_user

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/matches",
    tags=["matches"],
    responses={404: {"description": "Not found"}},
)

# Create JWT dependency instance
jwt_bearer = JWTBearer()

@router.post(
    "/",
    response_model=MatchResponse,
    summary="Match a load to available vehicles",
    description="Find the best matching vehicle for a given load, considering trailer compatibility.",
    dependencies=[Depends(jwt_bearer)]
)
async def create_match(
    request: Request,
    match_request: MatchRequest
):
    """
    Match a load to available vehicles.
    
    Parameters:
    - **load_id**: The ID of the load to match
    - **vehicle_ids**: Optional list of specific vehicle IDs to consider
    
    Returns:
    - Best matching vehicle with score and reasons
    - 404 error if no suitable match found
    """
    try:
        current_user = await get_current_user(request)
        logger.info(f"Creating match for load {match_request.load_id} by user {current_user['email']}")
        
        # Get match result from engine
        match_result = match_load_to_vehicle(
            load_id=match_request.load_id,
            vehicle_ids=match_request.vehicle_ids,
            user_id=current_user["email"]
        )
        
        if not match_result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No suitable vehicle found for the load"
            )
        
        logger.info(f"Successfully created match for load {match_request.load_id}")
        return match_result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating match: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

@router.get(
    "/{match_id}",
    response_model=MatchResponse,
    summary="Get match details",
    description="Retrieve details of a specific match.",
    dependencies=[Depends(jwt_bearer)]
)
async def get_match(
    request: Request,
    match_id: str
):
    """
    Get details of a specific match.
    
    Parameters:
    - **match_id**: The ID of the match to retrieve
    
    Returns:
    - Match details if found
    - 404 error if match not found
    """
    try:
        current_user = await get_current_user(request)
        logger.info(f"Retrieving match {match_id} for user {current_user['email']}")
        
        # TODO: In Sprint 9, this will fetch from database
        # For now, return mock data
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            detail="Match retrieval not implemented in Sprint 8"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving match: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        ) 