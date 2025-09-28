# src/logic.py
import bcrypt
from .db import DatabaseManager


# ---------------- USER LOGIC ----------------
class UserLogic:
    def __init__(self):
        self.db = DatabaseManager()
    
    def register(self, username: str, email: str, password: str):
        if not username or not email or not password:
            return {"error": "Username, email, and password are required"}

        if self.db.get_user_by_email(email):
            return {"error": "Email already exists"}

        hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        result = self.db.create_user(username, email, hashed_pw)
        
        # Fixed: Handle Supabase response structure
        if hasattr(result, 'error') and result.error:
            return {"error": str(result.error)}
        
        if result.data:
            return {"message": "User registered successfully", "user_id": result.data[0]["id"]}
        else:
            return {"error": "Failed to create user"}

    def login(self, email: str, password: str):
        if not email or not password:
            return {"error": "Email and password are required"}

        user = self.db.get_user_by_email(email)
        if not user:
            return {"error": "User not found"}

        try:
            # Check password
            if bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
                user_safe = user.copy()
                user_safe.pop("password", None)  # Remove password from response
                return {"message": "Login successful", "user": user_safe}
            else:
                return {"error": "Incorrect password"}
        except Exception as e:
            print(f"Login error: {e}")
            return {"error": "Login failed due to server error"}

    def update(self, user_id: int, username: str = None, email: str = None, password: str = None):
        user = self.db.get_user_by_id(user_id)
        if not user:
            return {"error": "User not found"}

        update_data = {}
        if username:
            update_data["username"] = username
        if email:
            existing = self.db.get_user_by_email(email)
            if existing and existing["id"] != user_id:
                return {"error": "Email already in use"}
            update_data["email"] = email
        if password:
            update_data["password"] = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        if not update_data:
            return {"error": "No data provided to update"}

        result = self.db.update_user(user_id, username, email, password)
        
        # Fixed: Handle Supabase response structure
        if hasattr(result, 'error') and result.error:
            return {"error": str(result.error)}
        
        return {"message": "User updated successfully"}

    def delete(self, user_id: int):
        if not self.db.get_user_by_id(user_id):
            return {"error": "User not found"}
        
        result = self.db.delete_user(user_id)
        
        # Fixed: Handle Supabase response structure
        if hasattr(result, 'error') and result.error:
            return {"error": str(result.error)}
        
        return {"message": "User deleted successfully"}


# ---------------- POST LOGIC ----------------
class PostLogic:
    def __init__(self):
        self.db = DatabaseManager()
    
    def create(self, user_id: int, content: str):
        if not content or not content.strip():
            return {"error": "Post content cannot be empty"}
        if not self.db.get_user_by_id(user_id):
            return {"error": "User not found"}
        
        result = self.db.create_post(user_id, content)
        
        # Fixed: Handle Supabase response structure
        if hasattr(result, 'error') and result.error:
            return {"error": str(result.error)}
        
        if result.data:
            return {"message": "Post created successfully", "post_id": result.data[0]["id"]}
        else:
            return {"error": "Failed to create post"}

    def get_all(self):
        posts = self.db.get_all_posts()
        return posts if posts else []

    def get(self, post_id: int):
        post = self.db.get_post_by_id(post_id)
        if not post:
            return {"error": "Post not found"}
        return post

    def update(self, post_id: int, content: str):
        post = self.db.get_post_by_id(post_id)
        if not post:
            return {"error": "Post not found"}
        if not content or not content.strip():
            return {"error": "Content cannot be empty"}
        
        result = self.db.update_post(post_id, content)
        
        # Fixed: Handle Supabase response structure
        if hasattr(result, 'error') and result.error:
            return {"error": str(result.error)}
        
        return {"message": "Post updated successfully"}

    def delete(self, post_id: int):
        if not self.db.get_post_by_id(post_id):
            return {"error": "Post not found"}
        
        result = self.db.delete_post(post_id)
        
        # Fixed: Handle Supabase response structure
        if hasattr(result, 'error') and result.error:
            return {"error": str(result.error)}
        
        return {"message": "Post deleted successfully"}


# ---------------- COMMENT LOGIC ----------------
class CommentLogic:
    def __init__(self):
        self.db = DatabaseManager()
    
    def create(self, user_id: int, post_id: int, content: str):
        if not content or not content.strip():
            return {"error": "Comment content cannot be empty"}
        if not self.db.get_user_by_id(user_id):
            return {"error": "User not found"}
        if not self.db.get_post_by_id(post_id):
            return {"error": "Post not found"}
        
        result = self.db.create_comment(user_id, post_id, content)
        
        # Fixed: Handle Supabase response structure
        if hasattr(result, 'error') and result.error:
            return {"error": str(result.error)}
        
        if result.data:
            return {"message": "Comment created successfully", "comment_id": result.data[0]["id"]}
        else:
            return {"error": "Failed to create comment"}

    def get(self, comment_id: int):
        comment = self.db.get_comment_by_id(comment_id)
        if not comment:
            return {"error": "Comment not found"}
        return comment

    def get_by_post(self, post_id: int):
        if not self.db.get_post_by_id(post_id):
            return {"error": "Post not found"}
        
        comments = self.db.get_comments_by_post(post_id)
        return comments if comments else []

    def update(self, comment_id: int, content: str):
        comment = self.db.get_comment_by_id(comment_id)
        if not comment:
            return {"error": "Comment not found"}
        if not content or not content.strip():
            return {"error": "Content cannot be empty"}
        
        result = self.db.update_comment(comment_id, content)
        
        # Fixed: Handle Supabase response structure
        if hasattr(result, 'error') and result.error:
            return {"error": str(result.error)}
        
        return {"message": "Comment updated successfully"}

    def delete(self, comment_id: int):
        if not self.db.get_comment_by_id(comment_id):
            return {"error": "Comment not found"}
        
        result = self.db.delete_comment(comment_id)
        
        # Fixed: Handle Supabase response structure
        if hasattr(result, 'error') and result.error:
            return {"error": str(result.error)}
        
        return {"message": "Comment deleted successfully"}