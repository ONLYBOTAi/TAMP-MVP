"""
Pydantic schemas for request/response models.
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr
from services.auth.models.user_model import UserRole

class TokenPayload(BaseModel):
    """Schema for decoded JWT token payload"""
    sub: str  # subject (user email)
    role: UserRole
    exp: datetime  # expiration timestamp

class Token(BaseModel):
    """Schema for token response"""
    access_token: str
    token_type: str

class UserBase(BaseModel):
    """Base user schema"""
    email: EmailStr
    role: UserRole

class UserCreate(UserBase):
    """Schema for user creation"""
    password: str

class UserLogin(BaseModel):
    """Schema for user login"""
    email: EmailStr
    password: str

class User(UserBase):
    """Schema for user response"""
    id: str
    is_active: bool = True

    class Config:
        from_attributes = True
        json_encoders = {  # Ensures UUID is serialized as string
            'UUID': lambda v: str(v)
        }
 