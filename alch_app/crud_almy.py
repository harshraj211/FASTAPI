from fastapi import FastAPI, HTTPException, status, Depends, Response
from pydantic import BaseModel
from alch_app import models
from alch_app.database import engine, get_db
from sqlalchemy.orm import session


models.Base.metadata.create_all(bind=engine)
app=FastAPI()

class Post(BaseModel):
    title:str
    content:str
    published:bool=True

#get main or home page
@app.get("/")
def root_endpoint():
    return("Yeahh this is the root page")

#get all post on /posts endpoint
@app.get("/posts")
def get_allpost(db: session=Depends(get_db)):
    posts=db.query(models.Post).all()
    return {"Here is your post":posts}


#get post by id on /posts/id
@app.get("/posts/{id}")
def get_id(id:int, db: session=Depends(get_db)):
    posts=db.query(models.Post).filter(models.Post.id==id).first()

    if not posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return {"Here is your request post": posts}


#to create a post on the /posts
@app.post("/posts")
def create_post(post:Post, db:session=Depends(get_db)):
    new_post=models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return {"Here is your created post":new_post}

#to delete a post by its id
@app.delete("/posts/{id}")
def delete_post(id:int, db:session=Depends(get_db)):
    delete_post=db.query(models.Post).filter(models.Post.id==id)

    if delete_post.first()==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist, hence it can't be deleted ")

    delete_post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

