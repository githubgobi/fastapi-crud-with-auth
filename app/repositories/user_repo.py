import uuid
from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from core.auth import generate_client_credentials, hash_token, verify_password
from models.oauth_client import OAuthClient
from models.oauth_token import OAuthToken
from models.user import User


class UserRepository:

    @staticmethod
    async def create(db: AsyncSession, user_data: dict) -> User:
        user = User(**user_data)
        db.add(user)
        await db.commit()
        await db.refresh(user)

        client_id, client_secret = generate_client_credentials()
        client = OAuthClient(
            client_id=client_id,
            client_secret=client_secret,
            user_id=user.id,
        )
        db.add(client)
        await db.commit()
        await db.refresh(client)
        return user

    @staticmethod
    async def get_by_email(db: AsyncSession, email: str) -> User | None:
        result = await db.execute(select(User).where(User.email == email))
        return result.scalars().first()

    @staticmethod
    async def login(db: AsyncSession, username: str, password: str) -> User:
        result = await db.execute(select(User).where(User.username == username))
        user = result.scalars().first()
        if not user:
            raise ValueError("Invalid username or password")
        if not verify_password(password, user.password):
            raise ValueError("Invalid username or password")
        return user

    @staticmethod
    async def get_client_credentials(db: AsyncSession, user_id: uuid.UUID) -> OAuthClient | None:
        result = await db.execute(select(OAuthClient).where(OAuthClient.user_id == user_id))
        return result.scalars().first()

    @staticmethod
    async def save_access_token(
        db: AsyncSession,
        user_id: uuid.UUID,
        access_token: str,
        refresh_token: str,
        client_id: uuid.UUID,
        expires_in: datetime,
    ) -> OAuthToken:
        result = await db.execute(select(OAuthToken).where(OAuthToken.user_id == user_id))
        token = result.scalars().first()

        if token:
            token.access_token = hash_token(access_token)
            token.refresh_token = hash_token(refresh_token)
            token.expires_in = expires_in
            token.updated_at = datetime.utcnow()
        else:
            token = OAuthToken(
                access_token=hash_token(access_token),
                refresh_token=hash_token(refresh_token),
                user_id=user_id,
                client_id=client_id,
                expires_in=expires_in,
            )
            db.add(token)

        await db.commit()
        await db.refresh(token)
        return token
