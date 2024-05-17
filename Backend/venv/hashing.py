from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
from fastapi import HTTPException, status
from .database import SessionLocal
from sqlalchemy.orm import Session
# from .models import User
from fastapi.security import OAuth2PasswordBearer

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

def get_hashed_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)