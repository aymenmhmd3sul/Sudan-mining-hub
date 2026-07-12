from datetime import datetime
from typing import Optional
from enum import Enum
import sqlalchemy as sa
from sqlmodel import SQLModel, Field, Column, String

class UserRole(str, Enum):
    ADMIN = "admin"
    MERCHANT = "merchant"
    BUYER = "buyer"
    AGENT = "agent"

class UserStatus(str, Enum):
    PENDING = "pending"
    ACTIVE = "active"
    SUSPENDED = "suspended"
    REJECTED = "rejected"

class User(SQLModel, table=True):
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(sa_column=Column(String, nullable=False))
    email: str = Field(sa_column=Column(String, unique=True, index=True, nullable=False))
    phone: str = Field(sa_column=Column(String, unique=True, index=True, nullable=False))
    password_hash: str = Field(sa_column=Column(String, nullable=False))
    role: UserRole = Field(default=UserRole.BUYER, sa_column=Column(String, nullable=False))
    status: UserStatus = Field(default=UserStatus.PENDING, sa_column=Column(String, nullable=False))
    country: str = Field(default="SD", sa_column=Column(String, nullable=False))
    language: str = Field(default="ar", sa_column=Column(String, nullable=False))
    created_at: datetime = Field(default_factory=datetime.utcnow, sa_column=Column(sa.DateTime, nullable=False))
    last_login: Optional[datetime] = Field(default=None, sa_column=Column(sa.DateTime, nullable=True))
    verified_at: Optional[datetime] = Field(default=None, sa_column=Column(sa.DateTime, nullable=True))
