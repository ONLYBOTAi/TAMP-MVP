# Auth Service

## Sprint 3 - JWT Auth Integration

### Features
- ✅ Token endpoints: `/register`, `/login`, `/validate-token`
- ✅ SQLAlchemy user model with Alembic migration
- ✅ Environment variables for secrets and DB
- ✅ FastAPI dependency injection (OAuth2Bearer)
- 🟡 Pending: integration tests

### Database Schema
- Users table with JWT-compatible fields
- Role-based access control (ADMIN, USER, DRIVER)
- Timestamps for auditing

### Setup
1. Create database:
```bash
PGPASSWORD=postgres createdb -h localhost -U postgres tamp_auth
```

2. Run migrations:
```bash
cd services/auth
alembic upgrade head
```

3. Start service:
```bash
uvicorn main:app --reload
```

### Environment Variables
Required in `.env`:
- `DATABASE_URL`: PostgreSQL connection string
- `JWT_SECRET_KEY`: Secret for JWT signing
- `JWT_ALGORITHM`: Algorithm for JWT (default: HS256)
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Token expiration time

### API Documentation
Visit `http://localhost:8000/docs` for Swagger UI documentation.

### Related Issues
- #12: "Integrate Kenny's JWT Auth Service" 