from sqlalchemy import Boolean,  Column, Integer, String,ForeignKey,Enum
from sqlalchemy.orm import relationship
from database.connection import Base
import enum

class Role(str, enum.Enum):
    superadmin = "superadmin"
    admin = "admin"
    user = "user"

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    password = Column(String(200), nullable=False)
    role = Column(Enum(Role), default=Role.user)

    posts = relationship("Post", back_populates="owner")

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    content = Column(String)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="posts")
    
   

 
