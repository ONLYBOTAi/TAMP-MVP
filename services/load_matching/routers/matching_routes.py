from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from schemas.matching import MatchRequest, MatchResponse, TruckMatch
from core.matcher import LoadMatcher
from services.auth.dependencies import get_current_user
from services.auth.schemas import User

router = APIRouter()
matcher = LoadMatcher()

@router.get("/match", response_model=List[TruckMatch])
async def get_matches(
    request: MatchRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Get available truck matches for a load request.
    
    Args:
        request: The load matching request containing origin, destination, and requirements
        current_user: The authenticated user making the request
        
    Returns:
        List of matching trucks with their details and match score
    """
    try:
        matches = await matcher.find_matches(request)
        if not matches:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No matching trucks found for the given criteria"
            )
        return matches
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.post("/request", response_model=MatchResponse)
async def create_match_request(
    request: MatchRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Create a new load matching request.
    
    Args:
        request: The load matching request details
        current_user: The authenticated user making the request
        
    Returns:
        The created match request with its status
    """
    try:
        response = await matcher.create_request(request, current_user)
        return response
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        ) 