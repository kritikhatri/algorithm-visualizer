import re

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from ..db import get_db
from ..models import User
from ..security import create_token, current_user, hash_password, verify_password

router = APIRouter(prefix="/api/auth", tags=["auth"])

EMAIL_RE = re.compile(r"^\S+@\S+\.\S+$")
USERNAME_RE = re.compile(r"^[A-Za-z0-9_]{3,20}$")


class RegisterBody(BaseModel):
    email: str
    username: str
    password: str


class LoginBody(BaseModel):
    email: str
    password: str


def public_user(user: User) -> dict:
    return {"id": user.id, "email": user.email, "username": user.username}


def auth_response(user: User) -> dict:
    return {"token": create_token(user.id), "user": public_user(user)}


@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(body: RegisterBody, db: Session = Depends(get_db)):
    email = body.email.strip().lower()
    username = body.username.strip()

    if not EMAIL_RE.match(email):
        raise HTTPException(400, "Enter a valid email address.")
    if not USERNAME_RE.match(username):
        raise HTTPException(400, "Username must be 3–20 letters, numbers or underscores.")
    if len(body.password) < 8:
        raise HTTPException(400, "Password must be at least 8 characters.")

    taken = db.scalar(select(User).where(or_(User.email == email, User.username == username)))
    if taken:
        raise HTTPException(409, "That email or username is already taken.")

    user = User(email=email, username=username, password_hash=hash_password(body.password))
    db.add(user)
    db.commit()
    return auth_response(user)


@router.post("/login")
def login(body: LoginBody, db: Session = Depends(get_db)):
    user = db.scalar(select(User).where(User.email == body.email.strip().lower()))
    if user is None or not verify_password(body.password, user.password_hash):
        raise HTTPException(401, "Incorrect email or password.")
    return auth_response(user)


@router.get("/me")
def me(user: User = Depends(current_user)):
    return {"user": public_user(user)}
