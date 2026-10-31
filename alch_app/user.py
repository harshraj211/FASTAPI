from fastapi import FastAPI, HTTPException, status, Depends, Response
from alch_app import models, schemas, utils
from alch_app.database import get_db, engine
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from .routers import users

models.Base.metadata.create_all(bind=engine)
app=FastAPI()
app.include_router(users.router)

@app.post("/users", response_model=schemas.UserOut)
def create_user(user:schemas.UserCreate,db: Session = Depends(get_db)):
    hashed_pass=utils.hash(user.password)
    user.password = hashed_pass

    new_user= models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@app.get("/users/{id}",response_model=schemas.UserOut)
def get_user(id:int, db: Session = Depends(get_db)):
    user=db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {id} does not exist in the database")
    return user
