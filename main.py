from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange

# Create an instance of the FastAPI application
app = FastAPI()


# Define the structure of a Post using Pydantic
class Post(BaseModel):
    title: str                  # Post title must be a string
    content: str                # Post content must be a string
    published: bool = True      # Defaults to True if not provided




# Temporary in-memory storage for posts
# Each post is stored as a dictionary
my_posts = [
    {
        "title": "title of post 1",
        "content": "content of post 1",
        "id": 1
    },
    {
        "title": "favourite foods",
        "content": "I like pizza",
        "id": 2
    }
]


# Find a post by its ID
def find_post(id, response=Response):
    for p in my_posts:
        # Return the post if its ID matches the given ID
        if p["id"] == id:
            return p

    # Returns None automatically if no matching post is found
def find_index_post(id):
    for i,p in enumerate(my_posts):
        if p['id']==id:
            return i


# Root endpoint: GET /
# Returns a welcome message
@app.get("/")
def read_root():
    return {"message": "Welcome to my ai!!"}


# GET /posts
# Returns all posts currently stored in memory
@app.get("/posts")
def get_posts():
    return {"data": my_posts}


# POST /posts
# Creates a new post using the JSON request body
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    # Convert the Pydantic model into a regular Python dictionary
    post_dict = post.model_dump()

    # Generate a random ID between 0 and 99999
    post_dict["id"] = randrange(0, 100000)

    # Add the new post to the in-memory list
    my_posts.append(post_dict)

    # Return the newly created post
    return {
        "data": post_dict
    }


# GET /posts/{id}
# Returns a specific post based on its ID
@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    # FastAPI converts the URL parameter to an integer
    print(id)

    # Search for the post with the given ID
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {id} don't exist in database")


    # Return the matching post
    return {"post_details": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int):
    #deleting_post
    #find the index in the array that has required id
    #my_post.pop(index)
    index= find_index_post(id)
    if index==None:
        raise  HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"User with id {id} does not exist so it cant be deleted")
    my_posts.pop(index)
    return {'message':'post was successfully deleted'}

@app.put("/posts/{id}", status_code=status.HTTP_200_OK)
def update_post(id: int, post:Post):
    index= find_index_post(id)
    if index==None:
        raise  HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"User with id {id} does not exist so it cant be updated")
    post_dict=post.model_dump()
    post_dict['id']=id
    my_posts[index]=post_dict
    return {"data":post_dict}
    # return {'message':'post successfully updated'}



