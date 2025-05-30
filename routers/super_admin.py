from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.models import User, Role
from database.schemas import UserOut,UserCreate
from dependencies import get_db, require_role
from auth import get_user_by_username, get_password_hash


router = APIRouter()

@router.get("/active-admin")
def get_active_admin(db: Session = Depends(get_db),user = Depends(require_role(Role.superadmin))):
    users = db.query(User).filter(User.is_active == True,User.role == 'admin').all()
    return {"count": len(users), "users": [f"{u.fname} {u.lname}" for u in users]}

@router.get("/admin", response_model=list[UserOut])
def list_admin(db: Session = Depends(get_db), user = Depends(require_role(Role.superadmin))):
    return db.query(User).filter(User.role=='admin').all()
    
@router.get("/admin/{user_id}",response_model=UserOut)
async def get_admin(id: str,db: Session = Depends(get_db), user = Depends(require_role(Role.superadmin))):
    try:
        user = db.query(User).filter(User.id == id,User.role == 'admin').first()
        
        if user is None:
            raise HTTPException(status_code=404, detail="Admin does not exist")
        
        return user
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Some error occured {e}")
  
@router.delete("/admin/{user_id}")
async def delete_admin(id: str,db: Session = Depends(get_db), user = Depends(require_role(Role.superadmin))):
    try:
        user = db.query(User).filter(User.id == id,User.role == 'admin').first()
        
        if user is None:
            raise HTTPException(status_code=404, detail="Admin does not exist")
        db.delete(user)
        db.commit()
        return {
            "status_code": 200,
            "data": "Deleted Admin",
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Some error occured {e}")
    
@router.put("/users/{user_id}/role")
def assign_role(user_id: str, new_role: Role, db: Session = Depends(get_db), user = Depends(require_role(Role.superadmin))):
    target_user = db.query(User).filter(User.id == user_id).first()
    if not target_user:
        raise HTTPException(status_code=404, detail="User not found")
    target_user.role = new_role
    db.commit()
    return {"msg": f"User role updated to {new_role}"}

@router.post("/createadmin")
def create_admin(new: UserCreate, 
                 new_role: Role,
                 user = Depends(require_role(Role.superadmin)),
                 db: Session = Depends(get_db)
                 ):
    db_user = get_user_by_username(db, new.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    if new.password != new.cpassword:
        raise HTTPException(status_code=400, detail="Password Missmatch")
    new_user = User(username=new.username,
                    fname = new.fname,
                    lname = new.lname,
                    email = new.email,
                    password=get_password_hash(new.password),
                    role = new_role)
    db.add(new_user)
    db.commit()
    return {"msg": f"{new_role} created"}