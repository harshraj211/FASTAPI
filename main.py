from fastapi import FastAPI
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
def find_post(id):
    for p in my_posts:
        # Return the post if its ID matches the given ID
        if p["id"] == id:
            return p

    # Returns None automatically if no matching post is found


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
@app.post("/posts")
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
def get_post(id: int):
    # FastAPI converts the URL parameter to an integer
    print(id)

    # Search for the post with the given ID
    post = find_post(id)

    # Return the matching post (or None if it doesn't exist)
    return {"post_details": post}