from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime , Boolean, Text
from sqlalchemy.dialects.postgresql import UUID
import uuid
from core.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String, nullable=False)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    email = Column(String, unique=True, index=True)
    password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(datetime, nullable=False)
    updated_at = Column(datetime, nullable=False)   

class OauthClient(Base):
    __tablename__ = "oauth_clients"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    client_id = Column(String, unique=True, index=True)
    client_secret = Column(String, nullable=False)
    user_id = Column(Integer, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(datetime, nullable=False)
    updated_at = Column(datetime, nullable=False)

class OauthToken(Base):
    __tablename__ = "oauth_tokens"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    access_token = Column(Text, unique=True)
    expires_in = Column(DateTime, nullable=False)
    user_id = Column(Integer, nullable=False)
    client_id = Column(UUID(as_uuid=True), nullable=False)
    created_at = Column(datetime, nullable=False)
    updated_at = Column(datetime, nullable=False)

