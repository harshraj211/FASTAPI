from fastapi import FastAPI,Response, status, HTTPException
from random import randrange
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import time

app=FastAPI()



class Post(BaseModel):
    title:str
    content:str
    published: bool = True

while True:
    try:
        conn= psycopg2.connect(host="localhost", database="Fastapi", user="postgres", password="2135", cursor_factory=RealDictCursor)
        cursor=conn.cursor()
        print("Successfull connection to the database")
        break
    except Exception as error:
        print("Connecting to database failed ")
        print("Error",error)
        time.sleep(5)

@app.get("/")
def root_endpoint():
    return ("This is the root endpoint")

@app.get("/posts")
def get_all_posts():
    conn.rollback()
    cursor.execute('SELECT * FROM public."POSTS"')
    posts=cursor.fetchall()
    return {"data": posts}

@app.get("/posts/{id}")
def get_one_post(id:int):
    conn.rollback()
    cursor.execute(
        'SELECT * from public."POSTS" WHERE "ID"=%s',
        (id,)
        )
    test_post=cursor.fetchone()
    if test_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not find in the database"
        )
    return {"post_details": test_post}

@app.post("/posts")
def create_post(post:Post, status_code=status.HTTP_201_CREATED):
    conn.rollback()
    cursor.execute(
        'INSERT INTO public."POSTS" ("TITLE", "CONTENT", "PUBLISHED") '
        'VALUES (%s,%s,%s) RETURNING *',
        (post.title, post.content, post.published)
    )
    new_post=cursor.fetchone()
    conn.commit()
    return {"Here is your created post": new_post}


@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int):
    conn.rollback()
    cursor.execute('DELETE FROM public."POSTS" WHERE "ID"=%s returning *',
                   (id,)
                   )
    deleted_post=cursor.fetchone()
    conn.commit()

    if delete_post==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist, hence it can't be deleted ")
    