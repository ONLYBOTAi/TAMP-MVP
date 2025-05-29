# TAMP-MVP

This is the MVP monorepo for the Truck Asset Matchmaking Platform (TAMP), built with containerized Python microservices using FastAPI and JWT authentication. It includes:

- 🚚 `vehicle-service`: secure CRUD API for truck listings  
- 🔐 `auth-service`: token-based role authentication (client, truck_owner, admin)  
- 📦 `shared/`: OpenAPI contracts and token utilities  
- 🧪 `tests/`: shell-based API regression tests  

## Getting Started

1. Clone this repo  
2. Copy `.env.sample` to `.env` in both services  
3. Run `docker compose -f docker-compose.dev.yml up --build`  
4. Execute `./tests/vehicle_tests.sh` to verify

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