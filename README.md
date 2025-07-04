# TAMP (Telematics and Asset Management Platform)

A microservices-based platform for managing telematics data and vehicle assets.

## Services

The platform consists of three main services:

1. **Auth Service** (Port 8000)
   - Handles user authentication and authorization
   - Swagger UI: http://127.0.0.1:8000/docs

2. **Vehicle Service** (Port 8001)
   - Manages vehicle information and metadata
   - Swagger UI: http://127.0.0.1:8001/docs

3. **Telematics Service** (Port 8002)
   - Processes and stores telematics data
   - Swagger UI: http://127.0.0.1:8002/docs

## Setup Instructions

1. Create and activate virtual environment:
   ```bash
   python3 -m venv tamp-venv
   source tamp-venv/bin/activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Start the services:
   ```bash
   # Auth Service
   cd services/auth
   uvicorn main:app --host 0.0.0.0 --port 8000

   # Vehicle Service
   cd services/vehicle
   uvicorn main:app --host 0.0.0.0 --port 8001

   # Telematics Service
   cd services/telematics
   uvicorn main:app --host 0.0.0.0 --port 8002
   ```

## Development

- Each service has its own directory under `services/`
- Common dependencies are managed in the root `requirements.txt`
- Use the Swagger UI endpoints to test API functionality
- Follow the microservices architecture pattern for new features

## Environment Variables

Each service requires its own `.env` file with appropriate configuration. See individual service directories for required variables.

## Testing

Run tests for each service:
```bash
cd services/<service-name>
pytest
```

## Git Strategy

- `main`: production  
- `dev`: active development  
- `feature/*`: per feature/user story  
- `hotfix/*`: emergency patches

## Architecture

The platform follows a microservices architecture with:

- **Authentication Service**: Handles user registration, login, and token validation
- **Vehicle Service**: Manages truck listings and owner verification
- **Shared Modules**: Common utilities and OpenAPI specifications

## Development

### Prerequisites

- Docker and Docker Compose
- Python 3.11+
- Git

### Local Development

1. Start the services:
   ```bash
   docker compose -f docker-compose.dev.yml up --build
   ```

2. Access the API documentation:
   - Auth Service: http://localhost:8000/docs
   - Vehicle Service: http://localhost:8001/docs

3. Run tests:
   ```bash
   ./tests/vehicle_tests.sh
   ```

## Contributing

1. Create a feature branch from `dev`
2. Make your changes
3. Submit a pull request to `dev`
4. Ensure all tests pass
5. Get code review approval

## License

Proprietary - © ONLYBOTAI 2024 

## Local Setup & Tests

1. Copy example env files:
   ```bash
   find services -type f -name ".env.example" -exec cp {} {}.env \;
   ```
Install dependencies:

```bash
python3 -m venv tamp-venv && source tamp-venv/bin/activate
pip install -r services/<your_service>/requirements.txt
```
Create Sprint 9 GitHub issues:

```bash
scripts/create_issues.sh
```
Run smoke tests locally:

```bash
docker compose -f docker-compose.dev.yml up -d --build
pytest tests/e2e/smoke_test.py
``` 