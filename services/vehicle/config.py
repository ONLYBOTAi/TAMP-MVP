from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    HOST: str = "0.0.0.0"
    PORT: int = 8001
    AUTH_SERVICE_URL: str = "http://tamp_auth_svc:8000"
    database_url: str = "postgresql://postgres:postgres@localhost:5432/tamp_vehicle"

    class Config:
        env_file = ".env"

settings = Settings() 