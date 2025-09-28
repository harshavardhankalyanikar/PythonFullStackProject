import streamlit as st
import requests
import time

API_URL = "http://127.0.0.1:8000"  # FastAPI backend URL

st.set_page_config(page_title="Social Media Network", page_icon="🌐")
st.title("🌐 Social Media Network")

# ---------------- SESSION STATE ----------------
if "user" not in st.session_state:
    st.session_state.user = None

# ---------------- HELPER FUNCTIONS ----------------
def safe_response(response):
    """Safely handle response JSON parsing"""
    try:
        return response.json()
    except Exception as e:
        st.error(f"Error parsing response: {e}")
        return {"error": f"Response parsing error: {response.status_code}"}


def register(username, email, password):
    """Register a new user"""
    try:
        response = requests.post(f"{API_URL}/register", json={
            "username": username,
            "email": email,
            "password": password
        }, timeout=10)
        return safe_response(response)
    except requests.exceptions.RequestException as e:
        return {"error": f"Connection error: {e}"}


def login(email, password):
    """Login user"""
    try:
        response = requests.post(f"{API_URL}/login", json={
            "email": email,
            "password": password
        }, timeout=10)
        return safe_response(response)
    except requests.exceptions.RequestException as e:
        return {"error": f"Connection error: {e}"}


def create_post(user_id, content):
    """Create a new post"""
    try:
        response = requests.post(f"{API_URL}/posts", json={
            "user_id": user_id,
            "content": content
        }, timeout=10)
        return safe_response(response)
    except requests.exceptions.RequestException as e:
        return {"error": f"Connection error: {e}"}


def update_post(post_id, content):
    """Update existing post"""
    try:
        response = requests.put(f"{API_URL}/posts/{post_id}", json={"content": content}, timeout=10)
        return safe_response(response)
    except requests.exceptions.RequestException as e:
        return {"error": f"Connection error: {e}"}


def delete_post(post_id):
    """Delete a post"""
    try:
        response = requests.delete(f"{API_URL}/posts/{post_id}", timeout=10)
        return safe_response(response)
    except requests.exceptions.RequestException as e:
        return {"error": f"Connection error: {e}"}


def get_posts():
    """Get all posts"""
    try:
        response = requests.get(f"{API_URL}/posts", timeout=10)
        return safe_response(response)
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to fetch posts: {e}")
        return []


def create_comment(user_id, post_id, content):
    """Create a new comment"""
    try:
        response = requests.post(f"{API_URL}/comments", json={
            "user_id": user_id,
            "post_id": post_id,
            "content": content
        }, timeout=10)
        return safe_response(response)
    except requests.exceptions.RequestException as e:
        return {"error": f"Connection error: {e}"}


def get_comments(post_id):
    """Get comments for a post"""
    try:
        response = requests.get(f"{API_URL}/comments/post/{post_id}", timeout=10)
        result = safe_response(response)
        # Handle both list and dict responses
        if isinstance(result, list):
            return result
        elif isinstance(result, dict) and "error" not in result:
            return result
        else:
            return []
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to fetch comments: {e}")
        return []


# ---------------- SIDEBAR ----------------
if st.session_state.user:
    st.sidebar.success(f"Logged in as: {st.session_state.user['username']}")
    if st.sidebar.button("Logout"):
        st.session_state.user = None
        st.rerun()

menu = ["Register", "Login", "Posts"] if not st.session_state.user else ["Posts", "Profile"]
choice = st.sidebar.selectbox("Menu", menu)


# ---------------- REGISTER ----------------
if choice == "Register" and not st.session_state.user:
    st.subheader("Create Account")
    
    with st.form("register_form"):
        username = st.text_input("Username", max_chars=20)
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")
        
        submit_register = st.form_submit_button("Register")
        
        if submit_register:
            if not username or not email or not password:
                st.error("All fields are required!")
            elif password != confirm_password:
                st.error("Passwords do not match!")
            elif len(password) < 6:
                st.error("Password must be at least 6 characters long!")
            else:
                with st.spinner("Creating account..."):
                    result = register(username, email, password)
                    if "error" in result:
                        st.error(result["error"])
                    else:
                        st.success("Account created successfully! Please login.")
                        time.sleep(1)
                        st.rerun()


# ---------------- LOGIN ----------------
elif choice == "Login" and not st.session_state.user:
    st.subheader("Login")
    
    with st.form("login_form"):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        
        submit_login = st.form_submit_button("Login")
        
        if submit_login:
            if not email or not password:
                st.error("Email and password are required!")
            else:
                with st.spinner("Logging in..."):
                    result = login(email, password)
                    if "error" in result:
                        st.error(result["error"])
                    elif "user" in result:
                        st.session_state.user = result["user"]
                        st.success("Logged in successfully!")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error(f"Unexpected login response: {result}")
                        st.write("Debug info:", result)  # For debugging


# ---------------- POSTS ----------------
elif choice == "Posts":
    if not st.session_state.user:
        st.warning("Please login to view or create posts.")
        st.info("Use the sidebar to navigate to Register or Login.")
    else:
        # Create Post Section
        st.subheader("Create a Post")
        with st.form("create_post_form"):
            post_content = st.text_area("What's on your mind?", max_chars=1000, height=100)
            submit_post = st.form_submit_button("Post")
            
            if submit_post:
                if not post_content.strip():
                    st.error("Post content cannot be empty.")
                else:
                    with st.spinner("Creating post..."):
                        res = create_post(st.session_state.user["id"], post_content)
                        if "error" in res:
                            st.error(res["error"])
                        else:
                            st.success("Post created successfully!")
                            time.sleep(1)
                            st.rerun()

        st.markdown("---")
        
        # Display Posts Section
        st.subheader("All Posts")
        
        with st.spinner("Loading posts..."):
            posts = get_posts()
        
        if not posts or (isinstance(posts, dict) and "error" in posts):
            st.info("No posts yet. Be the first to post something!")
        else:
            for i, post in enumerate(posts):
                with st.container():
                    # Post header
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.markdown(f"**User {post['user_id']}** • {post['date_posted'][:19]}")
                    with col2:
                        if post['user_id'] == st.session_state.user["id"]:
                            st.markdown("*Your post*")
                    
                    # Post content
                    st.markdown(f">{post['content']}")
                    
                    # Post actions (only for post owner)
                    if post['user_id'] == st.session_state.user["id"]:
                        with st.expander("✏️ Edit/Delete Post"):
                            new_content = st.text_area(
                                "Edit content:", 
                                value=post['content'], 
                                key=f"edit_{post['id']}_{i}",
                                max_chars=1000
                            )
                            
                            col1, col2 = st.columns(2)
                            with col1:
                                if st.button("Update Post", key=f"update_{post['id']}_{i}"):
                                    if not new_content.strip():
                                        st.error("Content cannot be empty!")
                                    else:
                                        with st.spinner("Updating..."):
                                            res = update_post(post['id'], new_content)
                                            if "error" in res:
                                                st.error(res["error"])
                                            else:
                                                st.success("Post updated!")
                                                time.sleep(1)
                                                st.rerun()
                            
                            with col2:
                                if st.button("🗑️ Delete Post", key=f"delete_{post['id']}_{i}", type="secondary"):
                                    if st.session_state.get(f"confirm_delete_{post['id']}", False):
                                        with st.spinner("Deleting..."):
                                            res = delete_post(post['id'])
                                            if "error" in res:
                                                st.error(res["error"])
                                            else:
                                                st.success("Post deleted!")
                                                time.sleep(1)
                                                st.rerun()
                                    else:
                                        st.session_state[f"confirm_delete_{post['id']}"] = True
                                        st.warning("Click again to confirm deletion")

                    # Comments Section
                    st.markdown("**💬 Comments:**")
                    
                    # Load comments
                    comments = get_comments(post['id'])
                    
                    if comments and isinstance(comments, list) and len(comments) > 0:
                        for comment in comments:
                            st.markdown(f"*User {comment['user_id']}*: {comment['content']}")
                            st.caption(f"Posted on {comment['date_commented'][:19]}")
                    else:
                        st.markdown("*No comments yet. Be the first to comment!*")
                    
                    # Add Comment Form
                    with st.form(f"comment_form_{post['id']}_{i}"):
                        comment_input = st.text_input(
                            "Add a comment:", 
                            key=f"comment_{post['id']}_{i}",
                            max_chars=500
                        )
                        submit_comment = st.form_submit_button("💬 Comment")
                        
                        if submit_comment:
                            if not comment_input.strip():
                                st.error("Comment cannot be empty.")
                            else:
                                with st.spinner("Adding comment..."):
                                    res = create_comment(st.session_state.user["id"], post['id'], comment_input)
                                    if "error" in res:
                                        st.error(res["error"])
                                    else:
                                        st.success("Comment added!")
                                        time.sleep(1)
                                        st.rerun()
                    
                    st.markdown("---")


# ---------------- PROFILE ----------------
elif choice == "Profile":
    if not st.session_state.user:
        st.warning("Please login to view your profile.")
    else:
        st.subheader("👤 User Profile")
        
        user = st.session_state.user
        
        col1, col2 = st.columns(2)
        with col1:
            st.info(f"**Username:** {user['username']}")
            st.info(f"**Email:** {user['email']}")
            st.info(f"**User ID:** {user['id']}")
        
        with col2:
            st.markdown("### Quick Stats")
            # You can add more stats here when you implement them
            st.metric("User ID", user['id'])
        
        st.markdown("---")
        st.markdown("### Account Actions")
        
        if st.button("🚪 Logout", type="secondary"):
            st.session_state.user = None
            st.success("Logged out successfully!")
            time.sleep(1)
            st.rerun()


# ---------------- FOOTER ----------------
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: gray; font-size: 0.8em;'>
    Social Media Network • Built with FastAPI & Streamlit • Powered by Supabase
    </div>
    """, 
    unsafe_allow_html=True
)