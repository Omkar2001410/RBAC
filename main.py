from fastapi import FastAPI, Depends, HTTPException, Body , UploadFile, File
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from database import schemas, models,connection
import auth,dependencies
from routers import auth_router, super_admin, admin, user

app = FastAPI()

models.Base.metadata.create_all(bind=connection.engine)

app.include_router(auth_router.router, tags=["Auth"])
app.include_router(super_admin.router, prefix="/superadmin", tags=["Superadmin"])
app.include_router(admin.router, prefix="/admin", tags=["Admin"])
app.include_router(user.router, prefix="/user", tags=["User"])

@app.get('/')
async def index():
    return {"Status": "Server running"}

