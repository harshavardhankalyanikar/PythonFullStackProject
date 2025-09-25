# src/logic.py
import bcrypt
from src.db import DatabaseManager

# ---------------- USER LOGIC ----------------
class UserLogic:
    def __init__(self):
        self.db=DatabaseManager()
    @staticmethod
    def register(self,username: str, email: str, password: str):
        if not username or not email or not password:
            return {"error": "Username, email, and password are required"}

        if self.db.get_user_by_email(email):
            return {"error": "Email already exists"}

        hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        result = self.db.create_user(username, email, hashed_pw)
        if result.error:
            return {"error": str(result.error)}
        return {"message": "User registered successfully", "user_id": result.data[0]["id"]}

    @staticmethod
    def login(self,email: str, password: str):
        if not email or not password:
            return {"error": "Email and password are required"}

        user = self.db.get_user_by_email(email)
        if not user:
            return {"error": "User not found"}

        if bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
            user_safe = user.copy()
            user_safe.pop("password", None)
            return {"message": "Login successful", "user": user_safe}
        return {"error": "Incorrect password"}

    @staticmethod
    def update(self,user_id: int, username: str = None, email: str = None, password: str = None):
        user = self.db.get_user_by_id(user_id)
        if not user:
            return {"error": "User not found"}

        data = {}
        if username: data["username"] = username
        if email:
            existing = self.db.get_user_by_email(email)
            if existing and existing["id"] != user_id:
                return {"error": "Email already in use"}
            data["email"] = email
        if password:
            data["password"] = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        if not data:
            return {"error": "No data provided to update"}

        return self.db.update_user(user_id, **data)

    @staticmethod
    def delete(self,user_id: int):
        if not self.db.get_user_by_id(user_id):
            return {"error": "User not found"}
        return self.db.delete_user(user_id)


# ---------------- POST LOGIC ----------------
class PostLogic:
    def __init__(self):
        self.db=DatabaseManager()
    @staticmethod
    def create(self,user_id: int, content: str):
        if not content:
            return {"error": "Post content cannot be empty"}
        if not self.db.get_user_by_id(user_id):
            return {"error": "User not found"}
        return self.db.create_post(user_id, content)

    @staticmethod
    def get_all(self):
        return self.db.get_all_posts()

    @staticmethod
    def get(self,post_id: int):
        post = self.db.get_post_by_id(post_id)
        if not post:
            return {"error": "Post not found"}
        return post

    @staticmethod
    def update(self,post_id: int, content: str):
        post = self.db.get_post_by_id(post_id)
        if not post:
            return {"error": "Post not found"}
        if not content:
            return {"error": "Content cannot be empty"}
        return self.db.update_post(post_id, content)

    @staticmethod
    def delete(self,post_id: int):
        if not self.db.get_post_by_id(post_id):
            return {"error": "Post not found"}
        return self.db.delete_post(post_id)


# ---------------- COMMENT LOGIC ----------------
class CommentLogic:
    def __init__(self):
        self.db=DatabaseManager()
    @staticmethod
    def create(self,user_id: int, post_id: int, content: str):
        if not content:
            return {"error": "Comment content cannot be empty"}
        if not self.db.get_user_by_id(user_id):
            return {"error": "User not found"}
        if not self.db.get_post_by_id(post_id):
            return {"error": "Post not found"}
        return self.db.create_comment(user_id, post_id, content)

    @staticmethod
    def get(self,comment_id: int):
        comment = self.db.get_comment_by_id(comment_id)
        if not comment:
            return {"error": "Comment not found"}
        return comment

    @staticmethod
    def get_by_post(self,post_id: int):
        if not self.db.get_post_by_id(post_id):
            return {"error": "Post not found"}
        return self.db.get_comments_by_post(post_id)

    @staticmethod
    def update(self,comment_id: int, content: str):
        comment = self.db.get_comment_by_id(comment_id)
        if not comment:
            return {"error": "Comment not found"}
        if not content:
            return {"error": "Content cannot be empty"}
        return self.db.update_comment(comment_id, content)

    @staticmethod
    def delete(self,comment_id: int):
        if not self.db.get_comment_by_id(comment_id):
            return {"error": "Comment not found"}
        return self.db.delete_comment(comment_id)