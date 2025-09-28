# Frontend ---> API ----> logic ----> db ---->Response
# api/main.py

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sys
import os

# Import manager from src
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.logic import UserLogic
from src.logic import PostLogic
from src.logic import CommentLogic

# -------------------App Setup-----------------
app = FastAPI(title="Social Media Network API", version="1.0")

# Initialize logic instances
user_logic = UserLogic()
post_logic = PostLogic()
comment_logic = CommentLogic()

# --------------------------Allow Frontend(Streamlit/React) to call the API------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------- MODELS ----------------
class RegisterModel(BaseModel):
    username: str
    email: str
    password: str


class LoginModel(BaseModel):
    email: str
    password: str


class UserUpdateModel(BaseModel):
    username: str = None
    email: str = None
    password: str = None


class PostModel(BaseModel):
    user_id: int
    content: str


class PostUpdateModel(BaseModel):
    content: str


class CommentModel(BaseModel):
    user_id: int
    post_id: int
    content: str


class CommentUpdateModel(BaseModel):
    content: str


# ---------------- USER ENDPOINTS ----------------
@app.post("/register")
def register_user(data: RegisterModel):
    result = user_logic.register(data.username, data.email, data.password)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result


@app.post("/login")
def login_user(data: LoginModel):
    result = user_logic.login(data.email, data.password)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result


@app.put("/users/{user_id}")
def update_user(user_id: int, data: UserUpdateModel):
    # Fixed: Use instance method instead of static method
    result = user_logic.update(user_id, data.username, data.email, data.password)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result


@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    # Fixed: Use instance method instead of static method
    result = user_logic.delete(user_id)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result


# ---------------- POST ENDPOINTS ----------------
@app.post("/posts")
def create_post(data: PostModel):
    # Fixed: Use instance method instead of static method
    result = post_logic.create(data.user_id, data.content)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result


@app.get("/posts")
def get_posts():
    # Fixed: Use instance method instead of static method
    return post_logic.get_all()


@app.get("/posts/{post_id}")
def get_post(post_id: int):
    # Fixed: Use instance method instead of static method
    result = post_logic.get(post_id)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result


@app.put("/posts/{post_id}")
def update_post(post_id: int, data: PostUpdateModel):
    # Fixed: Use instance method instead of static method
    result = post_logic.update(post_id, data.content)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result


@app.delete("/posts/{post_id}")
def delete_post(post_id: int):
    # Fixed: Use instance method instead of static method
    result = post_logic.delete(post_id)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result


# ---------------- COMMENT ENDPOINTS ----------------
@app.post("/comments")
def create_comment(data: CommentModel):
    # Fixed: Use instance method instead of static method
    result = comment_logic.create(data.user_id, data.post_id, data.content)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result


@app.get("/comments/{comment_id}")
def get_comment(comment_id: int):
    # Fixed: Use instance method instead of static method
    result = comment_logic.get(comment_id)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result


@app.get("/comments/post/{post_id}")
def get_comments_by_post(post_id: int):
    # Fixed: Use instance method instead of static method
    result = comment_logic.get_by_post(post_id)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result


@app.put("/comments/{comment_id}")
def update_comment(comment_id: int, data: CommentUpdateModel):
    # Fixed: Use instance method instead of static method
    result = comment_logic.update(comment_id, data.content)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result


@app.delete("/comments/{comment_id}")
def delete_comment(comment_id: int):
    # Fixed: Use instance method instead of static method
    result = comment_logic.delete(comment_id)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)