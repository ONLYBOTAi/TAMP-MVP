from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from sqlalchemy.orm import relationship
import enum

from .base import Base, TimestampMixin

class VehicleType(enum.Enum):
    CAR = "car"
    TRUCK = "truck"
    MOTORCYCLE = "motorcycle"
    BUS = "bus"
    OTHER = "other"

class Vehicle(Base, TimestampMixin):
    """Vehicle model for storing vehicle information."""
    __tablename__ = "vehicles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)  # Foreign key to auth.users
    make = Column(String(50), nullable=False)
    model = Column(String(50), nullable=False)
    year = Column(Integer, nullable=False)
    license_plate = Column(String(20), nullable=False, unique=True)
    vehicle_type = Column(Enum(VehicleType), nullable=False)
    color = Column(String(30))
    vin = Column(String(17), unique=True)  # Vehicle Identification Number

    def __repr__(self):
        return f"<Vehicle {self.make} {self.model} ({self.license_plate})>" 