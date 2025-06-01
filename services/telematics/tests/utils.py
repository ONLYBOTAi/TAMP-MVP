from datetime import datetime, timedelta
from jose import jwt
from core.config import get_settings

settings = get_settings()

def create_test_token(
    user_id: int = 1,
    expires_delta: timedelta = timedelta(minutes=15)
) -> str:
    """
    Create a test JWT token for testing purposes.
    
    Args:
        user_id: The user ID to encode in the token
        expires_delta: How long until the token expires
        
    Returns:
        str: A valid JWT token
    """
    expire = datetime.utcnow() + expires_delta
    to_encode = {
        "exp": expire,
        "sub": str(user_id)  # Convert to string as per JWT spec
    }
    return jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )

def create_expired_token(user_id: int = 1) -> str:
    """
    Create an expired JWT token for testing.
    
    Args:
        user_id: The user ID to encode in the token
        
    Returns:
        str: An expired JWT token
    """
    return create_test_token(
        user_id=user_id,
        expires_delta=timedelta(seconds=-1)
    ) 