from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from core.auth import verify_password ,hash_password
from models.user import User

class UserRepository:

    @staticmethod
    async def create(db: AsyncSession, user_data):
        user_data["password"] = hash_password(user_data["password"])
        user = User(**user_data)
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user
    
    @staticmethod
    async def get_by_email(db: AsyncSession, email: str):
        result = await db.execute(select(User).where(User.email == email))
        return result.scalars().first()
        
    @staticmethod
    async def login(db: AsyncSession, email: str, password: str):
        result = await db.execute(select(User).where(User.email == email))
        user = result.scalars().first()
        if not user:
            raise ValueError("Invalid email")
        
        if not verify_password(password, user.password):
            raise ValueError("Invalid email or password")
        
        return user