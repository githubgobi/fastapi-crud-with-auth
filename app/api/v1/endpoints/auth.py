from fastapi import APIRouter, Depends
from asyncio.log import logger
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import get_db
from schemas.user import UserCreate, UserLogin, UserResponse
from services.auth_service import register_user, login_user

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserResponse)
async def register(user: UserCreate, db: AsyncSession = Depends(get_db)):
    new_user = await register_user(db, user.name, user.email, user.password.get_secret_value())
    return UserResponse(id=new_user.id, name=new_user.name, email=new_user.email)

@router.post("/login", response_model=UserResponse)
async def login(user: UserLogin, db: AsyncSession = Depends(get_db)):
    login = await login_user(db, user.email, user.password.get_secret_value())
    return UserResponse(id=login.id, name=login.name, email=login.email)
