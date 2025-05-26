from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session,joinedload
from database.models import User, Role
from database.schemas import UserOut,UserPostOut, UserCreate
from dependencies import get_db, require_role
from auth import get_user_by_username, get_password_hash

router = APIRouter()

@router.get("/admin", response_model=list[UserOut])
def list_admin(db: Session = Depends(get_db), user = Depends(require_role(Role.superadmin))):
    return db.query(User).filter(User.role=='admin').all()

@router.get("/users", response_model=list[UserOut])
def list_users(db: Session = Depends(get_db), user = Depends(require_role(Role.superadmin))):
    return db.query(User).filter(User.role=='user').all()

@router.get("/Userdata", response_model=list[UserPostOut])
def user_data(db: Session = Depends(get_db),
               user = Depends(require_role(Role.superadmin))):
    try:
        return db.query(User).options(joinedload(User.posts)).filter(User.role == 'user').all()
    
    except Exception as e:
        raise HTTPException(status_code=200, detail=f"Empty")
    
@router.put("/users/{user_id}/role")
def assign_role(user_id: int, new_role: Role, db: Session = Depends(get_db), user = Depends(require_role(Role.superadmin))):
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
    new_user = User(username=new.username, password=get_password_hash(new.password))
    db.add(new_user)
    db.commit()
    return {"msg": "Admin created"}