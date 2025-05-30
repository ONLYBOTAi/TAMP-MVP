from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.pool import NullPool
import os

# Sync database URL for Alembic and direct queries
SYNC_DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://postgres:postgres@localhost:5432/tamp_vehicle"
)

# Async database URL for FastAPI async routes
ASYNC_DATABASE_URL = os.getenv(
    "ASYNC_DATABASE_URL",
    "postgresql+asyncpg://postgres:postgres@localhost:5432/tamp_vehicle"
)

# Sync engine and session
engine = create_engine(
    SYNC_DATABASE_URL,
    echo=True,
    poolclass=NullPool
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Async engine and session
async_engine = create_async_engine(
    ASYNC_DATABASE_URL,
    echo=True,
    future=True,
    poolclass=NullPool
)

async_session = sessionmaker(
    async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Sync session dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Async session dependency
async def get_async_db():
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close() 