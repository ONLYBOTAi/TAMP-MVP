"""
SQLAlchemy models for vehicle data.
"""

from datetime import datetime
from sqlalchemy import Column, String, Enum, DateTime, ForeignKey, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from uuid import uuid4
import enum
from models.base import Base  # Use relative import

class VehicleStatus(str, enum.Enum):
    """Vehicle status in the system."""
    ACTIVE = "active"
    INACTIVE = "inactive"
    MAINTENANCE = "maintenance"
    DELETED = "deleted"

class Vehicle(Base):  # Use shared Base
    """Vehicle model for truck owner's vehicles."""
    __tablename__ = "vehicles"

    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)

    # Vehicle information
    plate_number = Column(String, unique=True, index=True, nullable=False)
    make = Column(String, nullable=False)
    model = Column(String, nullable=False)
    year = Column(String, nullable=False)
    status = Column(Enum(VehicleStatus), default=VehicleStatus.ACTIVE, nullable=False)

    # Foreign key to owner (User)
    owner_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    owner = relationship("User", back_populates="vehicles")

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Indexes
    __table_args__ = (
        Index('idx_vehicles_owner_status', 'owner_id', 'status'),  # Composite index for owner+status queries
    )

    def __repr__(self):
        """String representation of the vehicle."""
        return f"<Vehicle {self.plate_number} ({self.make} {self.model})>" 