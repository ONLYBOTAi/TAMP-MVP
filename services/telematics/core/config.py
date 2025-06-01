from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    """Telematics service configuration settings."""
    PROJECT_NAME: str = "TAMP Telematics Service"
    VERSION: str = "0.1.0"
    API_V1_STR: str = "/api/v1"
    
    # Database settings
    DATABASE_URL: str = "sqlite:///./telematics.db"
    
    # Service settings
    SERVICE_PORT: int = 8003
    SERVICE_HOST: str = "0.0.0.0"
    
    # Authentication settings
    AUTH_SERVICE_URL: str = "http://auth-service:8000"
    SECRET_KEY: str = "your-secret-key-here"  # Change in production
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Telematics specific settings
    MAX_TELEMETRY_BATCH_SIZE: int = 100
    TELEMETRY_PROCESSING_INTERVAL: int = 60  # seconds
    
    # Alert thresholds
    SPEED_LIMIT: float = 120.0  # km/h
    ENGINE_TEMP_WARNING: float = 90.0  # celsius
    ENGINE_TEMP_CRITICAL: float = 100.0  # celsius
    BATTERY_VOLTAGE_LOW: float = 11.5  # volts
    FUEL_LEVEL_WARNING: float = 15.0  # percentage
    
    class Config:
        case_sensitive = True
        env_file = ".env"

@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings() 