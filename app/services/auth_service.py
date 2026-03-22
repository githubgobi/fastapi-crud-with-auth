from sqlalchemy.ext.asyncio import AsyncSession
from repositories.user_repo import UserRepository

async def register_user(db: AsyncSession, name: str, email: str, password: str):
    user_data = {"name": name, "email": email, "password": password}
    print("Registering user:", user_data)
    user = await UserRepository.create(db, user_data)
    return user

async def login_user(db: AsyncSession, email: str, password: str):
    user = await UserRepository.login(db, email, password)
    return user