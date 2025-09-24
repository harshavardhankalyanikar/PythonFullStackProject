#Social Network Backend (users, posts, comments)


This project is a backend implementation of a simple social networking platform built with Python, utilizing Supabase as the database and backend-as-a-service solution. It demonstrates key backend functionalities such as user management, content creation, and relational data handling through posts and comments.


## Features

** User Registration and Authentication:
Secure user registration with password hashing, and login validation to authenticate users.

** Post Creation:
Authenticated users can create posts containing textual content.

** Commenting System:
Users can comment on posts, enabling interaction and discussion within the platform.

** Data Storage and Retrieval:
Uses Supabase’s PostgreSQL database to store users, posts, and comments with proper relationships enforced via foreign keys.

** Secure Password Handling:
Passwords are securely hashed using bcrypt before storing, enhancing security.

** API-based Interaction:
The backend communicates with the Supabase database through its Python client library, abstracting direct SQL queries and simplifying API calls.


## Project structure
SocialMediaBackend/
|
|---src/          #core application logic
|   ---logic.py   #Business logic and task operations (user, posts, comments logic)
operations
|   ---db.py   #Database operations (Supabase client interactions)
|
|---api/     #Backend API
|   |---main.py #FastAPI endpoints FastAPI application and routes
|---frontend/   #frontend application
|   |---app.py   #streamlit web interface code
|---requirements.txt  #python dependencies
|---.env   #Python variables 
|---README.md   #project overview and instructions
# Quick Start

-Python 3.8 or higher
-A supabase account
-Git(push,cloning)


### 1.clone or Download the project

# option 1:clone with Git
git clone <repository url>
# option 2:Download and extract the ZIP file
 ### 2.Install Dependencies
 # Install all required python packages
 pip install -r requirements.txt


 ### 3.Setup supabase Database
 1.Create a supabase project:
 2. Create a Task  table:

- Go to the SQL Editor in your Supabase
dashboard
- Run this SQL command:
    
```sql
  -- Users table
CREATE TABLE "user" (
    id SERIAL PRIMARY KEY,
    username VARCHAR(20) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password VARCHAR(60) NOT NULL
);

-- Posts table
CREATE TABLE post (
    id SERIAL PRIMARY KEY,
    content TEXT NOT NULL,
    date_posted TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    user_id INTEGER NOT NULL REFERENCES "user"(id) ON DELETE CASCADE
);

-- Comments table
CREATE TABLE comment (
    id SERIAL PRIMARY KEY,
    content TEXT NOT NULL,
    date_commented TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    user_id INTEGER NOT NULL REFERENCES "user"(id) ON DELETE CASCADE,
    post_id INTEGER NOT NULL REFERENCES post(id) ON DELETE CASCADE
);
...
3. **Get Your Credentials**:


### 4. Configure Environment Variables


1. Create a '.env' file in the project root
2. Add your Supabase credentials to '.env':
SUPABASE_URL=your_project_url_here
SUPABASE_KEY=your_anon_key_here


**Example:**
SUPABASE_URL="https://abcd.supabase.co"
SUPABASE_KEY="sacyhtvgrytuyrebeVESEU66VCYCVTDXXYTUtrjtyreyvtu"

### 5. Run the Application


## Streamlit Frontend
streamlit run frontend/app.py

The app will open in your browser at 'https://localhost:8501'

## FastAPI Backend

cd api
python main.py

The API will be available at 'https://localhost:8000'

## How to Use

## Technical Details

### Technologies Used

-**Frontend**:Streamlit(python web framework)
- **Backend**:FastAPI(python REST API framework)
-**Database**:Supabase (postgreSQL-based backend-as-a-service)

-**Language**: Python 3.8+

### Key Components

1. **'src/db.py'**:Database operations 
    Handles all CRUD operations with Supabase
2. **'src/logic.py'**:Business logic
    - Task validation and processing


## Troubleshooting

#Common Issues

1.**"Module not found" errors**
    -Make sure you've installed all dependencies:`pip install -r requirements.txt`
    - Check that you're running commands from the correct directory

## Future Enhancements

Ideas for extending this project:

---**🧑‍💼 1. User Profiles & Avatars**:

Add a user profile table or extend the existing one with:

Bio, profile picture (upload to Supabase Storage)

Join date, location, website link

Allow users to update their profile

--**🔐 2. JWT Authentication**:

Implement token-based authentication using OAuth2 + JWT

Secure your FastAPI endpoints (e.g., require tokens for post/comment creation)

Use packages like fastapi-jwt-auth or fastapi-users
--**📨 3. Followers / Following System**:

Add a followers table to track relationships


Show user feeds based on who they follow

--**💬 4. Replies and Nested Comments**:

Add a parent_comment_id column in comments to allow threaded/nested replies

--**❤️ 5. Likes / Reactions**:

Add like/reaction tables for posts and comments

Store emoji-style reactions (👍 ❤️ 😂) if you want to expand later

--**🔍 6. Search & Filtering**:

Implement keyword search for posts

Filter by hashtags, date, or user

--**📂 7. Media Uploads (Images, Videos)**:

Use Supabase Storage to allow users to upload:

Profile pictures

Post images or videos

Store file URLs in your post table

--**📊 8. Analytics Dashboard (Admin or User)**:

Track number of posts, comments, likes

Show charts in Streamlit using plotly or altair

### support 
If you encounter any issues or have any questions:
--mobileno:7093006980
--email:harshavardhankalyanikar@gmail.com
