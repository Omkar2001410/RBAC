from sqlalchemy import Column, Integer, String, ForeignKey, Enum, DateTime, func, Boolean, Table
from sqlalchemy.orm import relationship
from database.connection import Base
import enum
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID
import uuid

class Role(str, enum.Enum):
    superadmin = "superadmin"
    admin = "admin"
    user = "user"

# auth_role_permissions = Table(
#     'role_permissions', Base.metadata,
#     Column('role_id',       Integer, ForeignKey('roles.id'),       primary_key=True),
#     Column('permission_id', Integer, ForeignKey('permissions.id'), primary_key=True),
# )

# auth_user_roles = Table(
#     'user_roles', Base.metadata,
#     Column('user_id', UUID, ForeignKey('users.id'), primary_key=True),
#     Column('role_id', Integer, ForeignKey('roles.id'), primary_key=True),
# )


class User(Base):
    __tablename__ = 'users'

    id = Column(UUID(as_uuid=True), primary_key=True, index=True,default=uuid.uuid4)
    username = Column(String(50), unique=True, index=True, nullable=False)
    fname = Column(String(50),index=True, nullable=False)
    lname = Column(String(50),index=True, nullable=False)
    email = Column(String(50),unique=True, index=True, nullable=False)
    password = Column(String(200), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)      
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    is_active = Column(Boolean, default=False)
    role = Column(Enum(Role), default=Role.user)
    # roles = relationship(
    #     'Role',
    #     secondary=auth_user_roles,
    #     back_populates='users'
    # )

    posts = relationship("Post", back_populates="owner")

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    content = Column(String)
    owner_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))

    owner = relationship("User", back_populates="posts")
    
   
class LogoutLog(Base):
    __tablename__ = "logout_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(UUID(as_uuid=True), nullable=False)
    logout_time = Column(DateTime(timezone=True), server_default=func.now())
 
# class Rol(Base):
#     __tablename__ = 'roles'
#     id          = Column(Integer, primary_key=True, index=True)
#     name        = Column(String, unique=True, nullable=False, index=True)
#     permissions = relationship(
#         'Permission',
#         secondary=auth_role_permissions,
#         back_populates='roles'
#     )

# class Permission(Base):
#     __tablename__ = 'permissions'
#     id    = Column(Integer, primary_key=True, index=True)
#     code  = Column(String, unique=True, nullable=False, index=True)
#     roles = relationship(
#         'Role',
#         secondary=auth_role_permissions,
#         back_populates='permissions'
#     )
# type(Role).users = relationship(
#     'User',
#     secondary=auth_user_roles,
#     back_populates='roles'
# )

