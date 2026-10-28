```python
# Import FastAPI to create the application
# Response allows us to return custom HTTP responses
# status provides predefined HTTP status codes
# HTTPException is used to return HTTP errors like 404 Not Found
from fastapi import FastAPI, Response, status, HTTPException

# Body is not currently used in this code
from fastapi.params import Body

# BaseModel is used to define and validate the structure of request data
from pydantic import BaseModel

# randrange generates a random integer for each new post ID
from random import randrange


# Create an instance of the FastAPI application
app = FastAPI()


# Define the structure of a Post using Pydantic
# FastAPI validates incoming JSON data against this model
class Post(BaseModel):
    title: str                  # Title of the post; must be a string
    content: str                # Content of the post; must be a string
    published: bool = True      # Optional field; defaults to True


# Temporary in-memory storage for posts
# Each post is represented as a Python dictionary
# Data is lost when the application restarts
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


# Helper function to find a post using its ID
def find_post(id, response=Response):
    # Loop through every post in the list
    for p in my_posts:
        # Check whether the current post's ID matches the given ID
        if p["id"] == id:
            return p  # Return the matching post

    # If no match is found, Python returns None automatically


# Helper function to find the INDEX of a post using its ID
# The index is the position of the post inside my_posts
def find_index_post(id):
    # enumerate() gives both the index (i) and the post (p)
    for i, p in enumerate(my_posts):
        # Compare the current post's ID with the requested ID
        if p["id"] == id:
            return i  # Return the index of the matching post

    # If no match is found, Python returns None automatically


# GET /
# Root endpoint: returns a welcome message
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
# Returns HTTP 201 Created when successful
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):

    # Convert the validated Pydantic model into a dictionary
    post_dict = post.model_dump()

    # Generate a random integer between 0 and 99999
    post_dict["id"] = randrange(0, 100000)

    # Add the new post dictionary to the list
    my_posts.append(post_dict)

    # Return the newly created post
    return {
        "data": post_dict
    }


# GET /posts/{id}
# Retrieves a single post using its ID from the URL
# Example: GET /posts/1
@app.get("/posts/{id}")
def get_post(id: int, response: Response):

    # FastAPI converts the URL path parameter to an integer
    print(id)

    # Search for a post with the requested ID
    post = find_post(id)

    # If the post doesn't exist, return HTTP 404 Not Found
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} don't exist in database"
        )

    # Return the matching post
    return {"post_details": post}


# DELETE /posts/{id}
# Deletes a post using its ID
# Example: DELETE /posts/1
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):

    # Find the index of the post that needs to be deleted
    index = find_index_post(id)

    # If no matching post exists, return HTTP 404 Not Found
    if index is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {id} does not exist so it cant be deleted"
        )

    # Remove the post at the specified index from the list
    my_posts.pop(index)

    # NOTE: HTTP 204 responses must not contain a response body.
    # Return None here, or use an explicit Response with status 204.


# PUT /posts/{id}
# Updates an existing post using its ID
# Example: PUT /posts/1
@app.put("/posts/{id}", status_code=status.HTTP_200_OK)
def update_post(id: int, post: Post):

    # Find the index of the post that needs to be updated
    index = find_index_post(id)

    # If the post doesn't exist, return HTTP 404 Not Found
    if index is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {id} does not exist so it cant be updated"
        )

    # Convert the validated request body into a dictionary
    post_dict = post.model_dump()

    # Preserve the ID from the URL instead of generating a new one
    post_dict["id"] = id

    # Replace the existing post at that index with the updated post
    my_posts[index] = post_dict

    # Return the updated post
    return {"data": post_dict}
```