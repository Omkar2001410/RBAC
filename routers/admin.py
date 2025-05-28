from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from database.models import User, Role, Post
from database.schemas import UserOut,UserPostOut
from dependencies import get_db, require_role

router = APIRouter()

@router.get("/active-users")
def get_active_users(db: Session = Depends(get_db),user = Depends(require_role(Role.admin))):
    users = db.query(User).filter(User.is_active == True,User.role == 'user').all()
    return {"count": len(users), "users": [f"{u.fname} {u.lname}" for u in users]}

@router.get("/users", response_model=list[UserOut])
def list_users(db: Session = Depends(get_db), user = Depends(require_role(Role.admin))):
    return db.query(User).filter(User.role == 'user').all()

    
@router.get("/Userdata", response_model=list[UserPostOut])
def user_data(db: Session = Depends(get_db),
               user = Depends(require_role(Role.admin))):
    try:
        return db.query(User).options(joinedload(User.posts)).filter(User.role == 'user').all()
    
    except Exception as e:
        raise HTTPException(status_code=200, detail=f"Empty")
    
@router.delete("/user/{user_id}")
async def delete_User(id: str,db: Session = Depends(get_db), user = Depends(require_role(Role.admin))):
    try:
        user = db.query(User).filter(User.id == id,User.role == 'user').first()
        
        if user is None:
            raise HTTPException(status_code=404, detail="User does not exist")
        db.delete(user)
        db.commit()
        return {
            "status_code": 200,
            "data": "Deleted User",
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Some error occured {e}")