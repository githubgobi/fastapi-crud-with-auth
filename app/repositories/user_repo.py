from datetime import datetime, timedelta

from schemas.user import OauthToken
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from core.auth import generate_client_credentials, hash_token, verify_password ,hash_password
from models.user import User, OAuthClient

class UserRepository:

    @staticmethod
    async def create(db: AsyncSession, user_data):
        user_data["password"] = hash_password(user_data["password"])
        user = User(**user_data)
        db.add(user)
        await db.commit()
        await db.refresh(user)
        client_id, client_secret = generate_client_credentials()
        client = OAuthClient(
            client_id=client_id,
            client_secret_hash=hash_password(client_secret),
            user_id=user.id
        )
        return user
    
    @staticmethod
    async def get_by_email(db: AsyncSession, email: str):
        result = await db.execute(select(User).where(User.email == email))
        return result.scalars().first()
        
    @staticmethod
    async def login(db: AsyncSession, username: str, password: str):
        result = await db.execute(select(User).where(User.name == username))
        user = result.scalars().first()
        if not user:
            raise ValueError("Invalid username")
        
        if not verify_password(password, user.password):
            raise ValueError("Invalid username or password")
        
        return user
        
    @staticmethod
    async def create_client(db: AsyncSession, user_id: int):
        client_id, client_secret = generate_client_credentials()
        client = OAuthClient(
            client_id=client_id,
            client_secret_hash=hash_password(client_secret),
            user_id=user_id
        )
        db.add(client)
        await db.commit()
        await db.refresh(client)
        return client_id, client_secret
        
    @staticmethod
    async def get_client(db: AsyncSession, client_id: str):
        result = await db.execute(select(OAuthClient).where(OAuthClient.client_id == client_id))
        return result.scalars().first()
    
    @staticmethod
    async def get_client_credentials(db: AsyncSession, user_id: int):
        result = await db.execute(select(OAuthClient).where(OAuthClient.user_id == user_id))
        return result.scalars().first()
    
    @staticmethod
    async def save_access_token(db: AsyncSession, user_id: int, access_token: str, refresh_token: str , client_id: str):
        # Implement logic to save access token and refresh token in the database
        # You may want to create a new model for storing tokens and add the necessary fields
        result = await db.execute(select(OauthToken).where(OauthToken.user_id == user_id))
        token = result.scalars().first()
        if token:
            access_token=hash_token(access_token.fresh_token),
            client_id=client_id,
            token.expires_in = access_token.expires_in  # Set expiration time as needed
        else:
            token = OauthToken(
                access_token=hash_token(access_token.fresh_token),
                user_id=user_id,
                client_id=client_id,
                expires_in=access_token.expires_in  # Set expiration time as needed
            )
            db.add(token)
        await db.commit()
        await db.refresh(token)
        return token