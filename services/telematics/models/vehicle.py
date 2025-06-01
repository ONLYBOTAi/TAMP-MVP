from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from core.database import Base

class Vehicle(Base):
    """Stub model for vehicle references."""
    __tablename__ = "vehicles"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    telemetry_data = relationship("TelemetryData", back_populates="vehicle")
    telemetry_alerts = relationship("TelemetryAlert", back_populates="vehicle") 