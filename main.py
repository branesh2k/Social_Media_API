from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

posts = []


class Post(BaseModel):
    title: str
    content: str
    published: bool = False


@app.get('/')
def homepage():
    return {"data: BLOG PAGE"}


@app.get('/posts')
def all_posts():
    print(posts)
    return posts


@app.post('/new_post')
def new_posts(post: Post):
     print(post)
     posts.append(post.dict())
     return {"data": post}
