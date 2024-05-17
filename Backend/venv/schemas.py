from pydantic import BaseModel, EmailStr, constr
from datetime import date

class Member(BaseModel):
    firstname: str
    lastname: str
    birthday: date
    address: str
    country: str
    eMail: EmailStr
    phoneNumber: constr(regex=r'^\+?1?\d{9,15}$')

class Account(BaseModel):
    login: str
    password: str

class AccountPage(BaseModel):
    user_name: str
