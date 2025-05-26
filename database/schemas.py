from pydantic import BaseModel
from enum import Enum

class Role(str, Enum):
    superadmin = "superadmin"
    admin = "admin"
    user = "user"

class UserCreate(BaseModel):
    username: str
    password: str
    

class UserOut(BaseModel):
    id: int
    username: str
    
    
    class Config:
        from_attributes = True

class PostCreate(BaseModel):
    title: str
    content: str
   

class PostOut(BaseModel):
    title: str
    content: str

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class PostUpdate(BaseModel):
    title: str
    content: str

class TokenRefresh(BaseModel):
    refresh_token: str


class UserPost(BaseModel):
    title: str
    content: str

    class Config:
        from_attributes = True

class UserPostOut(BaseModel):
    username: str
    posts: list[UserPost] =[]