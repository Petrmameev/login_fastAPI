import sqlite3
from datetime import datetime, timedelta, timezone
from sqlite3 import Connection
from typing import Optional

import bcrypt
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from pydantic import BaseModel

from config import *

app = FastAPI()


def get_db_connection() -> Connection:
    conn = sqlite3.connect(DATABASE_URL.split("///")[-1], check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


class User(BaseModel):
    username: str
    salary: float
    date_next_raise_salary: datetime


class UserInDb(User):
    hashed_password: str


def get_user(db: Connection, username: str) -> Optional[UserInDb]:
    cursor = db.cursor()
    user = cursor.execute(
        "SELECT * FROM users WHERE username = ?", (username,)
    ).fetchone()
    if user:
        return UserInDb(**user)
    return None


@app.post("/token")
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    users_db: Connection = Depends(get_db_connection),
):
    user = get_user(users_db, form_data.username)
    if not user or not bcrypt.checkpw(
        form_data.password.encode("utf-8"), user.hashed_password.encode("utf-8")
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный логин или пароль",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expire = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expire_delta=access_token_expire
    )
    return {"access_token": access_token, "token_type": "bearer"}


def create_access_token(data: dict, expire_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expire_delta:
        expire = datetime.now(timezone.utc) + expire_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.get("/salary")
async def read_salary(
    token: str = Depends(oauth2_scheme),
    users_db: Connection = Depends(get_db_connection),
):
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
    user = get_user(users_db, username)
    if user is None:
        raise credentials_exception
    return {
        "username": user.username,
        "salary": user.salary,
        "next_raise": user.date_next_raise_salary,
    }
