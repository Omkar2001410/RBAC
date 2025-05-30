from fastapi import FastAPI,Depends
from database import models,connection
from routers import auth_router, super_admin, admin, user
from database.models import *
from sqlalchemy.orm import Session
from dependencies import get_db

app = FastAPI()

models.Base.metadata.create_all(bind=connection.engine)

app.include_router(auth_router.router, tags=["Auth"])
app.include_router(super_admin.router, prefix="/superadmin", tags=["Superadmin"])
app.include_router(admin.router, prefix="/admin", tags=["Admin"])
app.include_router(user.router, prefix="/user", tags=["User"])

@app.get('/')
async def index():
    return {"Status": "Server running"}

# main.py (part 1)

@app.post("/init")
def init_data(db: Session = Depends(get_db)):
    # Create permissions
    p1 = Permission(code="admin.access")
    p2 = Permission(code="user.manage")
    p3 = Permission(code="profile.view")
    p4 = Permission(code = "post.view")
    p5 = Permission(code = "post.create")
    p6 = Permission(code = "post.delete")
    p7 = Permission(code = "post.update")

    # Create roles
    superadmin = Rol(name="superadmin", permissions=[p1, p2, p3,p4,p5,p6,p7])
    admin = Rol(name="admin", permissions=[p2, p3])
    user = Rol(name="user", permissions=[p3,p4,p5,p6,p7])

    # Create users
    

    db.add_all([p1, p2, p3,p4,p5,p6,p7, admin, superadmin,user])
    db.commit()
    return {"msg": "Initialized"}
