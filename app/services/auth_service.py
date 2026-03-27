import uuid

from sqlalchemy.ext.asyncio import AsyncSession
from repositories.user_repo import UserRepository
from core.auth import hash_password

async def register_user(db: AsyncSession, username: str, first_name: str, last_name: str, email: str, password: str):
    user_data = {
        "username": username,
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "password": hash_password(password),  # Hash the password
    }
    print("Registering user:", user_data)
    user = await UserRepository.create(db, user_data)
    return user

async def login_user(db: AsyncSession, username: str, password: str):
    user = await UserRepository.login(db, username, password)
    return user

async def get_client_credentials(db: AsyncSession, user_id: uuid.UUID):
    credentials = await UserRepository.get_client_credentials(db, user_id)
    return credentials

async def save_access_token(db: AsyncSession, user_id: uuid.UUID, access_token: str, refresh_token: str, client_id: str):
    # Implement logic to save access token and refresh token in the database
    token = await UserRepository.save_access_token(db, user_id, access_token, refresh_token, client_id)
    return token
