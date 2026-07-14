from datetime import datetime
from typing import Optional, List
from enum import Enum
import sqlalchemy as sa
from sqlmodel import SQLModel, Field, Relationship, Column, String, DateTime, Boolean

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
    __table_args__ = {'extend_existing': True}

    # 1. الحقول السيادية الأساسية (المطابقة لـ auth.py)
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    name: str = Field(sa_column=Column(String(150), nullable=False))
    email: str = Field(sa_column=Column(String(150), unique=True, index=True, nullable=False))
    phone: str = Field(sa_column=Column(String(50), unique=True, index=True, nullable=False))
    password_hash: str = Field(sa_column=Column(String(255), nullable=False))
    
    # 2. حقول الإدارة والحالة والمنشأ
    role: UserRole = Field(default=UserRole.BUYER, sa_column=Column(String(50), nullable=False))                                   
    status: UserStatus = Field(default=UserStatus.PENDING, sa_column=Column(String(50), nullable=False))                           
    country: str = Field(default="SD", sa_column=Column(String(10), nullable=False))      
    language: str = Field(default="ar", sa_column=Column(String(10), nullable=False))     
    
    # 3. حقول التتبع الزمني
    created_at: datetime = Field(default_factory=datetime.utcnow, sa_column=Column(DateTime, nullable=False))                  
    updated_at: datetime = Field(default_factory=datetime.utcnow, sa_column=Column(DateTime, nullable=False, onupdate=datetime.utcnow))                                       
    last_login: Optional[datetime] = Field(default=None, sa_column=Column(DateTime, nullable=True))
    verified_at: Optional[datetime] = Field(default=None, sa_column=Column(DateTime, nullable=True))                       

    # 4. حقول القدرات (Capabilities Flags) المطلوبة لملف app/security/policy.py
    is_active: bool = Field(default=True, sa_column=Column(Boolean, default=True, nullable=False))
    is_admin: bool = Field(default=False, sa_column=Column(Boolean, default=False, nullable=False))
    is_moderator: bool = Field(default=False, sa_column=Column(Boolean, default=False, nullable=False))
    is_seller: bool = Field(default=False, sa_column=Column(Boolean, default=False, nullable=False))
    is_importer: bool = Field(default=False, sa_column=Column(Boolean, default=False, nullable=False))
    is_global_provider: bool = Field(default=False, sa_column=Column(Boolean, default=False, nullable=False))

    # 5. متوافقات الخلفية (Backward Compatibility Properties) لضمان عدم انكسار الملفات القديمة
    @property
    def full_name(self) -> str:
        """جسر توافق للملفات التي تبحث عن full_name بدلاً من name"""
        return self.name

    @property
    def hashed_password(self) -> str:
        """جسر توافق للملفات التي تبحث عن hashed_password بدلاً من password_hash"""
        return self.password_hash
