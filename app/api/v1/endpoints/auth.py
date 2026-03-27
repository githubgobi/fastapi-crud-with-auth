from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from http.client import HTTPException
from fastapi import status
from asyncio.log import logger
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import get_db
from schemas.user import UserCreate, UserLogin, UserResponse ,TokenData, Token
from core.auth import create_access_token, create_refresh_token
from services.auth_service import register_user, login_user ,get_client_credentials, save_access_token

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserResponse)
async def register(user: UserCreate, db: AsyncSession = Depends(get_db)):
    new_user = await register_user(db, user.username, user.first_name, user.last_name, user.email, user.password.get_secret_value())
    return UserResponse(first_name=new_user.first_name, username=new_user.username, last_name=new_user.last_name, email=new_user.email)

@router.post("/login", response_model=Token)
async def login(user: UserLogin, db: AsyncSession = Depends(get_db)):
    login = await login_user(db, user.username, user.password.get_secret_value())

    if not login:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")
    
    credentials = await get_client_credentials(db, login.id)

    if not credentials:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials generated")
    
    token = create_access_token({"sub": login.id, "client_id": credentials.id})
    refresh_token = create_refresh_token()
    db_token = save_access_token(db, login.id, token, refresh_token,credentials.id)
    return Token(access_token=token, refresh_token=refresh_token, token_type="bearer")
