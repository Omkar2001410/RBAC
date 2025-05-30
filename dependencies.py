from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
import database.models as models, database.connection as connection
from dotenv import load_dotenv
import os
from database.models import *

load_dotenv()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

def get_db():
    db = connection.SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials"
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
        user = db.query(models.User).filter(models.User.username == username).first()
        if user is None:
            raise credentials_exception
        return user
    except JWTError:
        raise credentials_exception

def decode_token(token: str):
    return token  


def require_role(*allowed: models.Role):
    def checker(current_user = Depends(get_current_user)):
        role = current_user.role
        if role not in [r.value for r in allowed]:
            raise HTTPException(status.HTTP_403_FORBIDDEN, "Insufficient permissions")
        
    return checker

# def require_permission(permission_code: str):
#     def checker(user: User = Depends(get_current_user)):
#         user_perms = {
#             perm.code
#             for role in user.roles
#             for perm in role.permissions
#         }
#         if permission_code not in user_perms:
#             raise HTTPException(
#                 status_code=status.HTTP_403_FORBIDDEN,
#                 detail="Permission denied"
#             )
#     return checker