from datetime import date, timedelta
from typing import Optional, Union
from pydantic import BaseModel, EmailStr, constr, validator


class UserRegistration(BaseModel):
    firstname: str
    lastname: str
    birthday: str  # Date format in ISO (YYYY-MM-DD)
    email: str
    phone_number: str
    address: str
    country: str
    login_name: str
    password: str



class Member(BaseModel):
    firstname: str
    lastname: str
    birthday: date
    address: Optional[str] = None
    country: Optional[str] = None
    email: EmailStr
    phone_number: Optional[str] = None

    @validator('phone_number')
    def validate_phone_number(cls, phone_number):
        if phone_number and not phone_number.isdigit():
            raise ValueError("Phone number must contain only digits")
        return phone_number

    @validator('birthday')
    def validate_age(cls, birthday: date):
        min_age = 18
        if (date.today() - birthday) < timedelta(days=(min_age * 365.25)):
            raise ValueError(f"Member must be at least {min_age} years old!")
        return birthday


class Account(BaseModel):
    login_name: str
    hashed_password: str


class AccountPage(BaseModel):
    user_name: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None
