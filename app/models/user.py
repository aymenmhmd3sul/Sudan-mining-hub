from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime
from functools import cached_property
from app.models.role import user_roles

class User(Base):
    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(150), nullable=False)
    email = Column(String(150), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # العلاقات المستقرة
    roles = relationship('Role', secondary=user_roles, lazy='joined')
    memberships = relationship('Membership', back_populates='user', cascade='all, delete-orphan')

    @cached_property
    def permissions_set(self):
        perms = set()
        for role in self.roles:
            for perm in role.permissions:
                perms.add(perm.name)
        return perms
