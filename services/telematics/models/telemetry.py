from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from core.database import Base
from .vehicle import Vehicle

class TelemetryData(Base):
    """Model for storing vehicle telemetry data."""
    __tablename__ = "telemetry_data"

    id = Column(Integer, primary_key=True, index=True)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Location data
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    altitude = Column(Float)
    speed = Column(Float)  # km/h
    
    # Engine data
    engine_rpm = Column(Integer)
    fuel_level = Column(Float)  # percentage
    engine_temperature = Column(Float)  # celsius
    
    # Additional metrics
    battery_voltage = Column(Float)
    odometer = Column(Float)  # kilometers
    trip_distance = Column(Float)  # kilometers
    
    # Diagnostic data
    diagnostic_codes = Column(JSON)
    warning_lights = Column(JSON)
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    vehicle = relationship("Vehicle", back_populates="telemetry_data")

class TelemetryAlert(Base):
    """Model for storing telemetry-based alerts."""
    __tablename__ = "telemetry_alerts"

    id = Column(Integer, primary_key=True, index=True)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"), nullable=False)
    alert_type = Column(String, nullable=False)  # e.g., "SPEED", "ENGINE", "BATTERY"
    severity = Column(String, nullable=False)  # e.g., "INFO", "WARNING", "CRITICAL"
    message = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    resolved = Column(Integer, default=False)
    resolved_at = Column(DateTime)
    
    # Additional data
    context_data = Column(JSON)
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    vehicle = relationship("Vehicle", back_populates="telemetry_alerts") 