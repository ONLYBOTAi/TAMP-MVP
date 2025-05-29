# TAMP Vehicle Service

## Quickstart

1. **Environment Setup**
   ```bash
   # Create .env file
   echo "AUTH_SERVICE_URL=http://tamp_auth_svc:8000
   DATABASE_URL=postgresql://postgres:postgres@localhost:5432/tamp_vehicle" > .env
   ```

2. **Docker Setup**
   ```bash
   # Build and run
   docker compose -f docker-compose.dev.yml up --build
   ```

3. **Service Access**
   - API Documentation: http://localhost:8001/docs
   - Health Check: http://localhost:8001/health

## Token Usage

1. **Get Token from Auth Service**
   ```bash
   # Register
   curl -X POST http://localhost:8000/register -H "Content-Type: application/json" -d '{"username":"truck_owner", "password":"password", "role":"truck_owner"}'
   
   # Login
   curl -X POST http://localhost:8000/login -H "Content-Type: application/json" -d '{"username":"truck_owner", "password":"password"}'
   ```

2. **Use Token in Vehicle Service**
   ```bash
   # Create Vehicle
   curl -X POST http://localhost:8001/vehicles \
     -H "Authorization: Bearer <token>" \
     -H "Content-Type: application/json" \
     -d '{"plate_number":"ABC123", "make":"Toyota", "model":"Hilux", "year":2023, "capacity":2.5}'
   ```

## API Endpoints

### POST /vehicles
Create a new vehicle (requires truck_owner role)
- Request Body: Vehicle details
- Response: Created vehicle with ID

### GET /vehicles/mine
Get all vehicles owned by authenticated user
- Response: List of vehicles

## Testing

Run the test suite:
```bash
./tests/vehicle_tests.sh
```

Test cases cover:
- Token validation
- Role-based access
- Error handling
- Input validation

## Logging

The service uses two main log prefixes:
- 🔐 [AuthLog] - Authentication related logs
- 🛡️ [TokenGuard] - Security and token validation logs

## Overview
The Vehicle Service is part of the TAMP MVP platform, providing vehicle management functionality for truck owners.

## Features
- Vehicle registration and management
- Role-based access control (truck_owner only)
- JWT token validation
- Docker containerization

## Setup

### Prerequisites
- Docker and Docker Compose
- Python 3.11+
- Shared auth service running

### Environment Variables
The service uses the following environment variables (injected via Docker Compose):
```env
AUTH_SECRET_KEY=supersecretkey
PORT=8001
HOST=0.0.0.0
```

### Running the Service
1. Build and start the service:
```bash
docker-compose -f docker-compose.dev.yml up --build
```

2. The service will be available at `http://localhost:8001`

## Token Format
The service expects JWT tokens in the following format:
```json
{
    "sub": "user@example.com",
    "role": "truck_owner",
    "exp": 1723810922
}
```

## Error Handling
The service handles the following error cases:
- 401: Invalid or expired token
- 403: Missing role or insufficient permissions
- 422: Invalid request payload
- 500: Internal server error

## Development
- FastAPI for the web framework
- Pydantic for data validation
- Python-Jose for JWT handling
- Docker for containerization 