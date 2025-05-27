from pydantic import BaseModel
from enum import Enum

class Role(str, Enum):
    superadmin = "superadmin"
    admin = "admin"
    user = "user"

class UserCreate(BaseModel):
    username: str
    fname: str
    lname: str
    email: str
    password: str
    cpassword: str
    

class UserOut(BaseModel):
    id: int
    username: str
    fname: str
    lname: str
    email: str
    
    
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
    email : str
    posts: list[UserPost] =[]