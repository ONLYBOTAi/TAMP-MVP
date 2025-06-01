from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import logging
from schemas.auth_schema import UserCreate, User, Token, UserLogin
from models.user_model import User as UserModel
from core.security import hash_password, verify_password, create_access_token
from db.db import get_db

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["authentication"])

@router.post("/register", response_model=User)
async def register_user(user_in: UserCreate, db: AsyncSession = Depends(get_db)):
    try:
        # Check if user already exists
        logger.info(f"Checking if user {user_in.email} already exists")
        result = await db.execute(
            select(UserModel).where(UserModel.email == user_in.email)
        )
        if result.scalars().first():
            raise HTTPException(
                status_code=400,
                detail="Email already registered"
            )

        # Create new user
        logger.info(f"Creating new user with email {user_in.email}")
        new_user = UserModel(
            email=user_in.email,
            password=hash_password(user_in.password),
            role=user_in.role
        )
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
        logger.info(f"Successfully created user {user_in.email}")
        return new_user
    except Exception as e:
        logger.error(f"Error in register_user: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )

@router.post("/login", response_model=Token)
async def login_user(user_in: UserLogin, db: AsyncSession = Depends(get_db)):
    # Find user by email
    result = await db.execute(
        select(UserModel).where(UserModel.email == user_in.email)
    )
    user = result.scalars().first()
    
    # Verify credentials
    if not user or not verify_password(user_in.password, user.password):
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    # Generate JWT token
    token = create_access_token(
        data={"sub": user.email, "role": user.role}
    )
    return {"access_token": token, "token_type": "bearer"} 