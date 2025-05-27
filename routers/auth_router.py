from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.models import User, Role
from database.schemas import UserCreate, Token
from auth import  create_access_token, get_user_by_username, verify_password, get_password_hash, authenticate_user
from dependencies import get_db,get_current_user
from fastapi.security import OAuth2PasswordRequestForm


router = APIRouter()

@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_username(db, user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    if user.password != user.cpassword:
        raise HTTPException(status_code=400, detail="Password Missmatch")
    new_user = User(username=user.username,
                    fname = user.fname,
                    lname = user.lname,
                    email = user.email, 
                    password=get_password_hash(user.password))
    db.add(new_user)
    db.commit()
    return {"msg": "User created"}

@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token,"token_type": "bearer"}

@router.get("/protected")
def protected_route(current_user: User = Depends(get_current_user)):
    return {"message": f"Hello, {current_user.fname}!"}
