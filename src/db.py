import os
from supabase import create_client, Client
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


# ---------------- USERS ----------------
def create_user(username: str, email: str, password: str):
    """Insert a new user"""
    return supabase.table("user").insert({
        "username": username,
        "email": email,
        "password": password
    }).execute()


def get_user_by_id(user_id: int):
    """Get a user by ID"""
    response = supabase.table("user").select("*").eq("id", user_id).execute()
    return response.data[0] if response.data else None


def get_user_by_email(email: str):
    """Get a user by email"""
    response = supabase.table("user").select("*").eq("email", email).execute()
    return response.data[0] if response.data else None


def update_user(user_id: int, username: str = None, email: str = None, password: str = None):
    """Update user info"""
    data = {}
    if username: data["username"] = username
    if email: data["email"] = email
    if password: data["password"] = password
    return supabase.table("user").update(data).eq("id", user_id).execute()


def delete_user(user_id: int):
    """Delete a user"""
    return supabase.table("user").delete().eq("id", user_id).execute()


# ---------------- POSTS ----------------
def create_post(user_id: int, content: str):
    """Insert a new post"""
    return supabase.table("post").insert({
        "user_id": user_id,
        "content": content,
        "date_posted": datetime.time()
    }).execute()


def get_post_by_id(post_id: int):
    """Get a post by ID"""
    response = supabase.table("post").select("*").eq("id", post_id).execute()
    return response.data[0] if response.data else None


def get_all_posts():
    """Get all posts"""
    response = supabase.table("post").select("*").execute()
    return response.data


def update_post(post_id: int, content: str):
    """Update post content"""
    return supabase.table("post").update({
        "content": content,
        "date_posted": datetime.time()
    }).eq("id", post_id).execute()


def delete_post(post_id: int):
    """Delete a post"""
    return supabase.table("post").delete().eq("id", post_id).execute()


# ---------------- COMMENTS ----------------
def create_comment(user_id: int, post_id: int, content: str):
    """Insert a new comment"""
    return supabase.table("comment").insert({
        "user_id": user_id,
        "post_id": post_id,
        "content": content,
        "date_commented": datetime.time()
    }).execute()


def get_comment_by_id(comment_id: int):
    """Get a comment by ID"""
    response = supabase.table("comment").select("*").eq("id", comment_id).execute()
    return response.data[0] if response.data else None


def get_comments_by_post(post_id: int):
    """Get all comments for a post"""
    response = supabase.table("comment").select("*").eq("post_id", post_id).execute()
    return response.data


def update_comment(comment_id: int, content: str):
    """Update comment content"""
    return supabase.table("comment").update({
        "content": content,
        "date_commented": datetime.time()
    }).eq("id", comment_id).execute()


def delete_comment(comment_id: int):
    """Delete a comment"""
    return supabase.table("comment").delete().eq("id", comment_id).execute()
