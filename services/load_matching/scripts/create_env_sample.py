import os
from pathlib import Path

def create_env_sample():
    """Create .env.sample file with configuration variables"""
    env_content = """# Service Configuration
MATCH_SERVICE_HOST=0.0.0.0
MATCH_SERVICE_PORT=8003

# Authentication
MATCH_JWT_SECRET=changeme
MATCH_JWT_ALGORITHM=HS256
MATCH_ACCESS_TOKEN_EXPIRE_MINUTES=30

# Service URLs
MATCH_TELEMATICS_URL=http://tamp_telematics_svc:8002
MATCH_VEHICLE_SVC_URL=http://tamp_vehicle_svc:8001

# Matching Configuration
MATCH_MAX_DISTANCE_KM=500
MATCH_MIN_SCORE=0.6
MATCH_CAPACITY_BUFFER=0.1
MATCHING_THRESHOLD=0.75

# Logging
MATCH_LOG_LEVEL=INFO
MATCH_LOG_FORMAT=json

# Metrics
METRICS_ENABLED=true
MATCH_METRICS_PORT=9090
PROMETHEUS_MULTIPROC_DIR=/tmp/prometheus_multiproc

# Performance
MATCH_MAX_CONCURRENT_REQUESTS=100
MATCH_REQUEST_TIMEOUT=30
MATCH_RETRY_ATTEMPTS=3
MATCH_RETRY_DELAY=2

# Rate Limiting
RATE_LIMIT=100
RATE_LIMIT_PERIOD=60
RATE_LIMIT_BURST=200

# Development
MATCH_DEBUG=false
MATCH_TEST_MODE=false
"""
    
    # Create config directory if it doesn't exist
    config_dir = Path("services/load_matching/config")
    config_dir.mkdir(parents=True, exist_ok=True)
    
    # Write .env.sample file
    env_file = config_dir / ".env.sample"
    with open(env_file, "w") as f:
        f.write(env_content)
    
    print(f"Created .env.sample at {env_file}")

if __name__ == "__main__":
    create_env_sample() 