from sqlalchemy import Column, Integer, String,ForeignKey,Enum, DateTime, func
from sqlalchemy.orm import relationship
from database.connection import Base
import enum
from datetime import datetime

class Role(str, enum.Enum):
    superadmin = "superadmin"
    admin = "admin"
    user = "user"

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    fname = Column(String(50),index=True, nullable=False)
    lname = Column(String(50),index=True, nullable=False)
    email = Column(String(50),unique=True, index=True, nullable=False)
    password = Column(String(200), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)      
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    role = Column(Enum(Role), default=Role.user)

    posts = relationship("Post", back_populates="owner")

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    content = Column(String)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="posts")
    
   

 
