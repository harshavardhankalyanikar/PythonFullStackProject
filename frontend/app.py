import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"  # FastAPI backend URL

st.set_page_config(page_title="Social Media Network", page_icon="🌐")
st.title("🌐 Social Media Network")

# ---------------- SESSION STATE ----------------
if "user" not in st.session_state:
    st.session_state.user = None

# ---------------- HELPER FUNCTIONS ----------------
def safe_response(response):
    try:
        return response.json()
    except Exception:
        return {"status": response.status_code, "text": response.text}
def register(username, email, password):
    response = requests.post(f"{API_URL}/register", json={
        "username": username,
        "email": email,
        "password": password
    })
    return safe_response(response)



def login(email, password):
    response = requests.post(f"{API_URL}/login", json={
        "email": email,
        "password": password
    })
    return safe_response(response)


def create_post(user_id, content):
    response = requests.post(f"{API_URL}/posts", json={
        "user_id": user_id,
        "content": content
    })
    return response.json()


def update_post(post_id, content):
    response = requests.put(f"{API_URL}/posts/{post_id}", json={"content": content})
    return response.json()


def delete_post(post_id):
    response = requests.delete(f"{API_URL}/posts/{post_id}")
    return response.json()


def get_posts():
    response = requests.get(f"{API_URL}/posts")
    return response.json()


def create_comment(user_id, post_id, content):
    response = requests.post(f"{API_URL}/comments", json={
        "user_id": user_id,
        "post_id": post_id,
        "content": content
    })
    return response.json()


def get_comments(post_id):
    response = requests.get(f"{API_URL}/comments/post/{post_id}")
    return response.json()


# ---------------- SIDEBAR ----------------
menu = ["Register", "Login", "Posts"]
choice = st.sidebar.selectbox("Menu", menu)


# ---------------- REGISTER ----------------
if choice == "Register":
    st.subheader("Create Account")
    username = st.text_input("Username")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Register"):
        result = register(username, email, password)
        if "error" in result:
            st.error(result["error"])
        else:
            st.success(result.get("message"))


# ---------------- LOGIN ----------------
elif choice == "Login":
    st.subheader("Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        result = login(email, password)
        if "error" in result:
            st.error(result["error"])
        else:
            st.session_state.user = result["user"]
            st.success("Logged in successfully!")


# ---------------- POSTS ----------------
elif choice == "Posts":
    if not st.session_state.user:
        st.warning("Please login to view or create posts.")
    else:
        st.subheader("Create a Post")
        post_content = st.text_area("Post Content")
        if st.button("Add Post"):
            if not post_content.strip():
                st.warning("Post content cannot be empty.")
            else:
                res = create_post(st.session_state.user["id"], post_content)
                if "error" in res:
                    st.error(res["error"])
                else:
                    st.success("Post created successfully!")

        st.markdown("---")
        st.subheader("All Posts")

        posts = get_posts()
        if not posts:
            st.info("No posts yet.")
        else:
            for post in posts:
                st.markdown(f"**User {post['user_id']}** posted:")
                st.write(post['content'])
                st.write(f"*Posted on: {post['date_posted']}*")

                # Post actions
                with st.expander("Edit/Delete Post"):
                    new_content = st.text_area(f"Edit Post {post['id']}", value=post['content'], key=f"edit_{post['id']}")
                    if st.button("Update Post", key=f"update_{post['id']}"):
                        res = update_post(post['id'], new_content)
                        if "error" in res:
                            st.error(res["error"])
                        else:
                            st.success("Post updated successfully!")

                    if st.button("Delete Post", key=f"delete_{post['id']}"):
                        res = delete_post(post['id'])
                        if "error" in res:
                            st.error(res["error"])
                        else:
                            st.success("Post deleted successfully!")

                # Comments
                st.markdown("**Comments:**")
                comments = get_comments(post['id'])
                if comments:
                    for comment in comments:
                        st.write(f"User {comment['user_id']}: {comment['content']} (on {comment['date_commented']})")
                else:
                    st.write("No comments yet.")

                comment_input = st.text_input(f"Add comment to post {post['id']}", key=f"comment_{post['id']}")
                if st.button("Add Comment", key=f"add_comment_{post['id']}"):
                    if not comment_input.strip():
                        st.warning("Comment cannot be empty.")
                    else:
                        res = create_comment(st.session_state.user["id"], post['id'], comment_input)
                        if "error" in res:
                            st.error(res["error"])
                        else:
                            st.success("Comment added successfully!")
