from fastapi import FastAPI, HTTPException, Response, status, Depends, APIRouter
from sqlalchemy.orm import Session
from ..import models, schemas , utils
from ..database import get_db

router=APIRouter(
    prefix="/posts",
    tags=['posts']
)

@router.get("/")
def root_endpoint():
    return("Yeahh this is the root page")

#get all post on /posts endpoint
@router.get("/", response_model=list[schemas.PostResponse])
def get_allpost(db: Session=Depends(get_db)):
    posts=db.query(models.Post).all()
    return posts


#get post by id on /posts/id
@router.get("/{id}",response_model=schemas.PostResponse)
def get_id(id:int, db: Session=Depends(get_db)):
    posts=db.query(models.Post).filter(models.Post.id==id).first()

    if not posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return posts


#to create a post on the /posts
@router.post("/", response_model=schemas.PostResponse)
def create_post(post:schemas.PostCreate, db:Session=Depends(get_db)):
    new_post=models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post

#to delete a post by its id
@router.delete("/{id}")
def delete_post(id:int, db:Session=Depends(get_db)):
    delete_post=db.query(models.Post).filter(models.Post.id==id)

    if delete_post.first()==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist, hence it can't be deleted ")

    delete_post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


