from fastapi import FastAPI, Depends, HTTPException, Body , UploadFile , APIRouter
from sqlalchemy.orm import Session
from database import schemas, models,connection
import dependencies
from database.models import Role


router = APIRouter()

models.Base.metadata.create_all(bind=connection.engine)


@router.post("/posts")
def create_post(
    post: schemas.PostCreate,
    db: Session = Depends(dependencies.get_db),
    current_user: models.User = Depends(dependencies.get_current_user),
    user = Depends(dependencies.require_role(Role.user))
):
    db_post = models.Post(**post.dict(), owner_id=current_user.id)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

@router.put("/posts/{post_id}")
async def update_post(
    post_id: str,
    db: Session = Depends(dependencies.get_db), 
    current_user: models.User = Depends(dependencies.get_current_user),
    update_post: schemas.PostUpdate = Body(...),
    user = Depends(dependencies.require_role(Role.user))
    ):
    post = db.query(models.Post).filter(models.Post.id == post_id, models.Post.owner_id == current_user.id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    for key, value in update_post.model_dump(exclude_unset=True).items():
        setattr(post, key, value)

    db.commit()
    db.refresh(post)
    return post

@router.delete("/posts/{post_id}")
async def delete_Post(
    post_id: str,
    db: Session = Depends(dependencies.get_db), 
    current_user: models.User = Depends(dependencies.get_current_user),
    user = Depends(dependencies.require_role(Role.user))
    ):
    try:
        post = db.query(models.Post).filter(models.Post.id == post_id, models.Post.owner_id == current_user.id).first()
        
        if post is None:
            raise HTTPException(status_code=404, detail="Task does not exist")
        db.delete(post)
        db.commit()
        return {
            "status_code": 200,
            "data": "Deleted Post",
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Some error occured {e}")
    

@router.get("/posts", response_model=list[schemas.PostOut])
def read_posts(db: Session = Depends(dependencies.get_db),
               current_user: models.User = Depends(dependencies.get_current_user),
               user = Depends(dependencies.require_role(Role.user))):
    try:
        return db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()
    
    except Exception as e:
        raise HTTPException(status_code=200, detail=f"Post not found")
    