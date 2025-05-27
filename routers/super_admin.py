from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session,joinedload
from database.models import User, Role,Post
from database.schemas import UserOut,UserPostOut, UserCreate, PostUpdate
from dependencies import get_db, require_role
from auth import get_user_by_username, get_password_hash

router = APIRouter()

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
    

    
@router.get("/users", response_model=list[UserOut])
def list_users(db: Session = Depends(get_db), user = Depends(require_role(Role.superadmin))):
    return db.query(User).filter(User.role=='user').all()

@router.get("/user/{user_id}",response_model=UserOut)
async def get_user(id: str,db: Session = Depends(get_db), user = Depends(require_role(Role.superadmin))):
    try:
        user = db.query(User).filter(User.id == id,User.role == 'user').first()
        
        if user is None:
            raise HTTPException(status_code=404, detail="User does not exist")
        
        return user
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Some error occured {e}")

@router.delete("/user/{user_id}")
async def delete_User(id: str,db: Session = Depends(get_db), user = Depends(require_role(Role.superadmin))):
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

@router.get("/Userdata", response_model=list[UserPostOut])
def user_data(db: Session = Depends(get_db),
               user = Depends(require_role(Role.superadmin))):
    try:
        return db.query(User).options(joinedload(User.posts)).filter(User.role == 'user').all()
    
    except Exception as e:
        raise HTTPException(status_code=200, detail=f"Empty")
    
@router.put("/posts/{post_id}")
async def update_post(
    post_id: str,
    db: Session = Depends(get_db), 
    update_post: PostUpdate = Body(...),
    user = Depends(require_role(Role.superadmin))
    ):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    for key, value in update_post.model_dump(exclude_unset=True).items():
        setattr(post, key, value)

    db.commit()
    db.refresh(post)
    return post
    
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