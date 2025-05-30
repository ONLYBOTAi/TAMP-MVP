"""
SQLAlchemy models for user data.
"""

from datetime import datetime
from sqlalchemy import Column, String, Enum, DateTime, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from uuid import uuid4
import enum
from services.auth.models.base import Base  # Use shared Base

class UserRole(str, enum.Enum):
    """User roles in the system."""
    CLIENT = "client"
    TRUCK_OWNER = "truck_owner"
    AGENT = "agent"
    ADMIN = "admin"
    FLEET_MANAGER = "fleet_manager"

class User(Base):  # Use shared Base
    """User model for authentication and authorization."""
    __tablename__ = "users"

    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)

    # User information
    email = Column(String, unique=True, index=True, nullable=False)  # Changed to unique=True and removed primary_key
    password = Column(String, nullable=False)
    role = Column(Enum(UserRole), nullable=False)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships - using string reference to avoid circular imports
    vehicles = relationship(
        "Vehicle",
        back_populates="owner",
        cascade="all, delete-orphan",
        lazy="selectin"  # Eager loading for better performance
    )

    # Indexes
    __table_args__ = (
        Index('idx_users_role_email', 'role', 'email'),  # Composite index for role+email queries
    )

    def __repr__(self):
        """String representation of the user."""
        return f"<User {self.email} ({self.role})>" 