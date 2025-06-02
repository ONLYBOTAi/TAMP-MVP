import asyncio
import structlog
from datetime import datetime
from typing import Dict, Any
from pydantic import BaseModel
from tenacity import retry, stop_after_attempt, wait_fixed

logger = structlog.get_logger()

class TelemetryData(BaseModel):
    vehicle_id: str
    timestamp: datetime
    data: Dict[str, Any]
    metadata: Dict[str, Any] = None

@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
async def process_telemetry_data(data: Dict[str, Any], metadata: Dict[str, Any] = None):
    """
    Process telemetry data asynchronously with retry logic.
    This function is called by the background task in the API endpoint.
    
    Args:
        data: The telemetry data to process
        metadata: Additional metadata about the request (user, vehicle info, etc.)
    """
    try:
        current_time = datetime.utcnow()
        logger.info(
            "starting_telemetry_processing",
            vehicle_id=data.get("vehicle_id"),
            timestamp=current_time.isoformat(),
            metadata=metadata,
            telemetry=data
        )

        # Simulate processing time
        await asyncio.sleep(1)

        logger.info(
            "completed_telemetry_processing",
            vehicle_id=data.get("vehicle_id"),
            timestamp=current_time.isoformat(),
            processing_time=(datetime.utcnow() - current_time).total_seconds(),
            telemetry=data
        )

    except Exception as e:
        logger.error(
            "telemetry_processing_error",
            vehicle_id=data.get("vehicle_id"),
            timestamp=datetime.utcnow().isoformat(),
            error=str(e),
            error_type=type(e).__name__,
            telemetry=data
        )
        raise 