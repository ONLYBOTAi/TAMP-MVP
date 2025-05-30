"""
Shared SQLAlchemy declarative base for all models.
This ensures all models are registered under the same metadata,
allowing foreign keys and relationships to work correctly.
"""

from sqlalchemy.orm import declarative_base

Base = declarative_base() 