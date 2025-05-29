import os


class Config:
    AUTH_SERVICE_URL = os.getenv(
        "AUTH_SERVICE_URL",
        "http://tamp_auth_svc:8000"
    )


config = Config()
