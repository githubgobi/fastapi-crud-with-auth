import uuid
from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from core.auth import hash_password
from repositories.user_repo import UserRepository


async def register_user(
    db: AsyncSession,
    username: str,
    first_name: str,
    last_name: str,
    email: str,
    password: str,
):
    user_data = {
        "username": username,
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "password": hash_password(password),
    }
    return await UserRepository.create(db, user_data)


async def login_user(db: AsyncSession, username: str, password: str):
    return await UserRepository.login(db, username, password)


async def get_client_credentials(db: AsyncSession, user_id: uuid.UUID):
    return await UserRepository.get_client_credentials(db, user_id)


async def save_access_token(
    db: AsyncSession,
    user_id: uuid.UUID,
    access_token: str,
    refresh_token: str,
    client_id: uuid.UUID,
    expires_in: datetime,
):
    return await UserRepository.save_access_token(
        db, user_id, access_token, refresh_token, client_id, expires_in
    )
