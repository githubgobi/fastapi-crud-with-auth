from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.auth import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token, create_refresh_token
from core.database import get_db
from schemas.user import Token, UserCreate, UserLogin, UserResponse
from services.auth_service import get_client_credentials, login_user, register_user, save_access_token

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user: UserCreate, db: AsyncSession = Depends(get_db)):
    new_user = await register_user(
        db,
        user.username,
        user.first_name,
        user.last_name,
        user.email,
        user.password.get_secret_value(),
    )
    return UserResponse(
        username=new_user.username,
        first_name=new_user.first_name,
        last_name=new_user.last_name,
        email=new_user.email,
    )


@router.post("/login", response_model=Token)
async def login(user: UserLogin, db: AsyncSession = Depends(get_db)):
    try:
        logged_in_user = await login_user(db, user.username, user.password.get_secret_value())
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exc))

    credentials = await get_client_credentials(db, logged_in_user.id)
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="OAuth client not found for user",
        )

    expires_at = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token({
        "sub": str(logged_in_user.id),
        "client_id": str(credentials.id),
    })
    refresh_token = create_refresh_token()

    await save_access_token(
        db,
        logged_in_user.id,
        access_token,
        refresh_token,
        credentials.id,
        expires_at,
    )

    return Token(access_token=access_token, refresh_token=refresh_token, token_type="bearer")
