from jose import JWTError, jwt
from datetime import datetime, timedelta

#SECRET_KEY
#ALGORITHM
#EXPIRATION time

SECRET_KEY = "09bdjbwjbjwbcj6378YHlPcuVVtulxK0TH9ZTIMvP4Y2UWkmD0"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_TIME=30

def create_access_token(data: dict):
    to_encode = data.copy()
    expire=datetime.now()+ timedelta(minutes=ACCESS_TOKEN_EXPIRE_TIME)
    to_encode.update({"exp":expire})

    token=jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return token