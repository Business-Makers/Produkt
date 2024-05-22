from pydantic import BaseModel, EmailStr
from typing import Optional

class UserRegistration(BaseModel):
    firstname: str
    lastname: str
    birthday: str
    email: EmailStr
    phone_number: Optional[str]
    address: Optional[str]
    country: Optional[str]
    login_name: str
    password: str

class LoginCredentials(BaseModel):
    login_name: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
