# Vehicle Service

## ✅ Sprint 3 Progress

### Database Integration
- ✅ Alembic migrations configured and working
- ✅ Vehicles table created with proper schema
- ✅ SQLAlchemy session management implemented
- ✅ Real database queries replacing mock data

### Authentication
- ✅ JWT token validation integrated
- ✅ Role-based access control for vehicle creation
- ✅ Bearer token authentication for all endpoints

### API Endpoints
- ✅ GET /vehicles - List all vehicles (auth protected)
- ✅ POST /vehicles - Create new vehicle (truck owner only)

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- PostgreSQL 12+
- Docker (optional)

### Environment Variables
```env
DATABASE_URL=postgresql+psycopg2://postgres:postgres@localhost:5432/tamp_vehicle
ASYNC_DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/tamp_vehicle
AUTH_SERVICE_URL=http://localhost:8000
```

### Installation
1. Create virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run migrations:
   ```bash
   alembic upgrade head
   ```

4. Start the service:
   ```bash
   uvicorn main:app --reload
   ```

## 📚 API Documentation

Once running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 🔒 Authentication

All endpoints require a valid JWT token in the Authorization header:
```
Authorization: Bearer <token>
```

## 🧪 Testing

Run tests with:
```bash
pytest
```

## 📝 License

MIT 