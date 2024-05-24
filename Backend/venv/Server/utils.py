"""
Utils File

This file contains utility functions and variables used throughout the application.
"""
import bcrypt
from datetime import timedelta, datetime
from jose import jwt
from typing import Optional
from fastapi.security import OAuth2PasswordBearer

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
SECRET_KEY = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
"""
The secret key used for signing the JWT.
This key should be kept confidential and not hard-coded in production environments.
"""
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
"""
OAuth2 password flow dependency.
This is used to retrieve the token from the request and validate it. 
The 'tokenUrl' specifies the endpoint where the client can obtain the token.
"""


def get_hashed_password(password: str) -> str:
    """
    Hashes a password with bcrypt.

    Parameters:
        - password (str): The plaintext password to be hashed.

    Returns:
        str: The hashed password.
    """
    password_bytes = password.encode('utf-8')
    hashed = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
    return hashed.decode('utf-8')


def verify_password(plain_password: str, hashed_password_from_db: str) -> bool:
    """
    Verify a plain password against a hashed password.

    Parameters:
        - plain_password (str): The plaintext password provided for verification.
        - hashed_password_from_db (str): The hashed password retrieved from the database.

    Returns:
        bool: True if the plain password matches the hashed password, False otherwise.
    """
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password_from_db.encode('utf-8'))


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Creates a JWT access token.

    Parameters:
        - data (dict): The data payload to be encoded into the token.
        - expires_delta (timedelta, optional): The expiration time delta for the token (default: 15 minutes).

    Returns:
        str: The encoded JWT access token.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
