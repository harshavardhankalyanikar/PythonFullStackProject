import os
from supabase import create_client, Client
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Check if environment variables are loaded
if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set in environment variables")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


class DatabaseManager:
    # ---------------- USERS ----------------
    @staticmethod
    def create_user(username: str, email: str, password: str):
        """Insert a new user"""
        try:
            return supabase.table("user").insert({
                "username": username,
                "email": email,
                "password": password
            }).execute()
        except Exception as e:
            print(f"Database error in create_user: {e}")
            raise

    @staticmethod
    def get_user_by_id(user_id: int):
        """Get a user by ID"""
        try:
            response = supabase.table("user").select("*").eq("id", user_id).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Database error in get_user_by_id: {e}")
            return None

    @staticmethod
    def get_user_by_email(email: str):
        """Get a user by email"""
        try:
            response = supabase.table("user").select("*").eq("email", email).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Database error in get_user_by_email: {e}")
            return None

    @staticmethod
    def update_user(user_id: int, username: str = None, email: str = None, password: str = None):
        """Update user info"""
        try:
            data = {}
            if username:
                data["username"] = username
            if email:
                data["email"] = email
            if password:
                data["password"] = password
            
            if not data:
                return {"error": "No data to update"}
            
            return supabase.table("user").update(data).eq("id", user_id).execute()
        except Exception as e:
            print(f"Database error in update_user: {e}")
            raise

    @staticmethod
    def delete_user(user_id: int):
        """Delete a user"""
        try:
            return supabase.table("user").delete().eq("id", user_id).execute()
        except Exception as e:
            print(f"Database error in delete_user: {e}")
            raise

    # ---------------- POSTS ----------------
    @staticmethod
    def create_post(user_id: int, content: str):
        """Insert a new post"""
        try:
            return supabase.table("post").insert({
                "user_id": user_id,
                "content": content,
                "date_posted": datetime.now().isoformat()
            }).execute()
        except Exception as e:
            print(f"Database error in create_post: {e}")
            raise

    @staticmethod
    def get_post_by_id(post_id: int):
        """Get a post by ID"""
        try:
            response = supabase.table("post").select("*").eq("id", post_id).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Database error in get_post_by_id: {e}")
            return None

    @staticmethod
    def get_all_posts():
        """Get all posts ordered by date (newest first)"""
        try:
            response = supabase.table("post").select("*").order("date_posted", desc=True).execute()
            return response.data if response.data else []
        except Exception as e:
            print(f"Database error in get_all_posts: {e}")
            return []

    @staticmethod
    def update_post(post_id: int, content: str):
        """Update post content"""
        try:
            return supabase.table("post").update({
                "content": content,
                "date_posted": datetime.now().isoformat()  # Update timestamp
            }).eq("id", post_id).execute()
        except Exception as e:
            print(f"Database error in update_post: {e}")
            raise

    @staticmethod
    def delete_post(post_id: int):
        """Delete a post"""
        try:
            return supabase.table("post").delete().eq("id", post_id).execute()
        except Exception as e:
            print(f"Database error in delete_post: {e}")
            raise

    # ---------------- COMMENTS ----------------
    @staticmethod
    def create_comment(user_id: int, post_id: int, content: str):
        """Insert a new comment"""
        try:
            return supabase.table("comment").insert({
                "user_id": user_id,
                "post_id": post_id,
                "content": content,
                "date_commented": datetime.now().isoformat()
            }).execute()
        except Exception as e:
            print(f"Database error in create_comment: {e}")
            raise

    @staticmethod
    def get_comment_by_id(comment_id: int):
        """Get a comment by ID"""
        try:
            response = supabase.table("comment").select("*").eq("id", comment_id).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Database error in get_comment_by_id: {e}")
            return None

    @staticmethod
    def get_comments_by_post(post_id: int):
        """Get all comments for a post ordered by date"""
        try:
            response = supabase.table("comment").select("*").eq("post_id", post_id).order("date_commented", desc=False).execute()
            return response.data if response.data else []
        except Exception as e:
            print(f"Database error in get_comments_by_post: {e}")
            return []

    @staticmethod
    def update_comment(comment_id: int, content: str):
        """Update comment content"""
        try:
            return supabase.table("comment").update({
                "content": content,
                "date_commented": datetime.now().isoformat()  # Update timestamp
            }).eq("id", comment_id).execute()
        except Exception as e:
            print(f"Database error in update_comment: {e}")
            raise

    @staticmethod
    def delete_comment(comment_id: int):
        """Delete a comment"""
        try:
            return supabase.table("comment").delete().eq("id", comment_id).execute()
        except Exception as e:
            print(f"Database error in delete_comment: {e}")
            raise