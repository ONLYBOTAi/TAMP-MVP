from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
import os

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: int = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=expires_delta or 30)
    to_encode.update({"exp": expire})
    return jwt.encode(
        to_encode,
        os.getenv("AUTH_SECRET_KEY", "changeme"),
        algorithm=os.getenv("AUTH_ALGORITHM", "HS256")
    ) 