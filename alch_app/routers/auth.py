from fastapi import APIRouter, HTTPException, Depends, status, Response
from sqlalchemy.orm import Session
from ..database import get_db
from .. import schemas, models, utils
from . import oauth
from fastapi.security.oauth2 import OAuth2PasswordRequestForm


router=APIRouter(tags=['Authentication'])
@router.post('/login')
def login(user_credentials:OAuth2PasswordRequestForm=Depends(),db: Session = Depends(get_db)):
    #username=
    #password=
    user=db.query(models.User).filter(models.User.email==user_credentials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials")
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,details=f"Invalid Credentials")

    access_token= oauth.create_access_token(data={"user_id":user.id})
    
    return {"access_token":access_token, "token_type":"bearer"}