import sqlite3
from datetime import datetime, timedelta
from fastapi import FastAPI, Request, Form, HTTPException, status
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from typing import Annotated

app = FastAPI()

app.mount("/static", StaticFiles(directory="static", html=True), name="static")
templates = Jinja2Templates(directory="frontend")

# SQLite database file path
database_file = "data/database.db"

# Connect to the SQLite database
conn = sqlite3.connect('your.db', check_same_thread=False)
cursor = conn.cursor()

# Create the tables
create_tables_query = """
CREATE TABLE IF NOT EXISTS users (
    userID INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS loginLog (
    loginID INTEGER PRIMARY KEY AUTOINCREMENT,
    token TEXT NOT NULL,
    loginDateTime DATETIME NOT NULL,
    userID INTEGER NOT NULL,
    FOREIGN KEY (userID) REFERENCES users (userID)
);
"""
cursor.executescript(create_tables_query)

# Insert dummy user data
insert_data_query = """
INSERT INTO users (username, password) VALUES 
('username1', 'password1'),
('username2', 'password2')
ON CONFLICT (username) DO NOTHING;
"""
cursor.executescript(insert_data_query)

# Commit the changes
conn.commit()

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    query = "SELECT * FROM users WHERE username = ?"
    params = (username,)
    cursor.execute(query, params)
    user = cursor.fetchone()
    if user is None:
        raise credentials_exception
    return {"userId":user[0], "username":user[1]}


@app.on_event("shutdown")
def shutdown():
    # Close the cursor and connection
    cursor.close()
    conn.close()

@app.get("/", response_class=HTMLResponse)
async def login_page(request: Request):
    try:
        return templates.TemplateResponse("login.html", {"request": request})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/user")   
async def test(request: Request, user: dict = Depends(get_current_user)):
    return user
  
@app.post("/login")
def login(request: Request, username: str = Form(...), password: str = Form(...)):
    # Parameterized query to prevent SQL injection
    query = "SELECT * FROM users WHERE username = ? AND password = ?"
    params = (username, password)

    cursor.execute(query, params)
    result = cursor.fetchone()

    if result:
        token_data = {
            "id":username,
            "password":password
        }
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": username}, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

