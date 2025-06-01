import logging
from typing import Optional
from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class VehicleServiceError(Exception):
    """Base exception for vehicle service errors."""
    def __init__(self, message: str, status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)

class VehicleNotFoundError(VehicleServiceError):
    """Raised when a vehicle is not found."""
    def __init__(self, vehicle_id: int):
        super().__init__(
            f"Vehicle with ID {vehicle_id} not found",
            status.HTTP_404_NOT_FOUND
        )

class DatabaseError(VehicleServiceError):
    """Raised when a database operation fails."""
    def __init__(self, operation: str, error: SQLAlchemyError):
        super().__init__(
            f"Database error during {operation}: {str(error)}",
            status.HTTP_500_INTERNAL_SERVER_ERROR
        )

def handle_db_error(operation: str, error: SQLAlchemyError) -> None:
    """Handle database errors with proper logging."""
    logger.error(f"Database error during {operation}: {str(error)}")
    raise DatabaseError(operation, error)

def handle_not_found(vehicle_id: int) -> None:
    """Handle vehicle not found errors with proper logging."""
    logger.warning(f"Vehicle not found: {vehicle_id}")
    raise VehicleNotFoundError(vehicle_id)

def handle_auth_error(message: str) -> None:
    """Handle authentication errors with proper logging."""
    logger.error(f"Authentication error: {message}")
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=message
    ) 