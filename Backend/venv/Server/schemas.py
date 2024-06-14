"""
Pydantic Schemas File

This file contains Pydantic models representing data schemas used for validation and serialization.
"""
from fastapi import HTTPException
from pydantic import BaseModel, EmailStr, ValidationError,Field, validator
from typing import Optional
from sqlalchemy import DateTime
from models import AccountPages_Info


class LoginCredentials(BaseModel):
    """
    Model for login credentials.

    This Pydantic model represents the schema for user login credentials.
    It defines the structure and data types of the login_name and password fields.

    Attributes:
        - login_name (str): The username for login.
        - password (str): The password for login.
    """
    login_name: str
    password: str


class Token(BaseModel):
    """
    Model for an access token.

    This Pydantic model represents the schema for an access token.
    It defines the structure and data types of the access_token and token_type fields.

    Attributes:
        - access_token (str): The access token string.
        - token_type (str): The type of the token.
    """
    access_token: str = Field(..., min_length=10,
                              description="The access token string, must be at least 10 characters long.")
    token_type: str


class TokenData(BaseModel):
    """
    Model for token data.

    This Pydantic model represents the schema for token data.
    It defines the structure and data types of the username field.

    Attributes:
        - username (str, optional): The username extracted from the token data.
    """
    username: Optional[str] = Field(None, min_length=3,
                                    description="The username extracted from the token data, must be at least 3 characters long if provided.")


class UserRegistration(BaseModel):
    """
    Model for user registration details.

    This Pydantic model represents the schema for user registration details.
    It defines the structure and data types of various user registration fields.

    Attributes:
        - firstname (str): The first name of the user.
        - lastname (str): The last name of the user.
        - birthday (str): The birthday of the user.
        - eMail (Emailstr): The email address of the user.
        - phone_number (str, optional): The phone number of the user (optional).
        - address (str, optional): The address of the user (optional).
        - country (str, optional): The country of the user (optional).
        - login_name (str): The login name chosen by the user.
        - password (str): The password chosen by the user.
    """
    firstname: str = Field(..., min_length=3)
    lastname: str = Field(..., min_length=3)
    birthday: str
    eMail: EmailStr
    phone_number: Optional[str] = None
    address: Optional[str] = None
    country: Optional[str] = None
    login_name: str
    password: str

    @validator('login_name')
    def validate_login_name(cls, v):
        if len(v) < 3:
            raise ValueError('Login name must be at least 3 characters long.')
        if not v.isalnum():
            raise ValueError('Login name must be alphanumeric.')
        return v

    @validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long.')
        if not any(char.isdigit() for char in v):
            raise ValueError('Password must contain at least one digit.')
        if not any(char.isalpha() for char in v):
            raise ValueError('Password must contain at least one letter.')
        return v


class PasswordResetRequest(BaseModel):
    """
        Represents a request to reset a password.

        Attributes:
            token (Token): The reset token.
            new_password (str): The new password to set.
        """
    token: Token
    new_password: str


def validate_user_registration(data):
    try:
        user = UserRegistration(**data)
    except ValidationError as e:
        raise HTTPException(status_code=422, detail={"message": "Validation failed", "errors": e.errors()})


class ApiKeyCreation(BaseModel):
    """
        Represents the necessary API key information for connecting to a cryptocurrency exchange.

        Attributes:
            account_holder (str): A descriptive name for the API key.
            exchange_name (str): The identifier of the exchange (e.g., 'binance', 'kraken').
            key (str): The API key for the exchange.
            secret_key (str): The API secret key for the exchange.
            passphrase (str): The API passphrase for the exchange, if required.
        """

    account_holder: str
    exchange_name: str
    key: str
    secret_key: str
    passphrase: Optional[str] = None


class AcoountPages_Info_Validate(BaseModel):
    """
    AccountPagesInfo is a Pydantic base class that stores information about the account,
    including the balance, the number of currencies, the last updated date, and the ID of the associated AccountPages.

    Attributes:
        balance (float): The account balance. Must be non-negative.
        currency_count (int): The number of different currencies in the account. Must be non-negative.
        last_updated (datetime): The date and time of the last update. Defaults to the current time.
        account_page_id (int): The ID of the associated AccountPages. Must not be None.
    """
    balance: float
    currency_count: int
    last_updated: DateTime
    account_page_id: int

    @validator('balance')
    def validate_balance(cls, value):
        if value < 0:
            raise ValueError("Balance must be non-negative")
        return value

    class Config:
        arbitrary_types_allowed = True

    def validate_currency_count(cls, value):
        if value < 0:
            raise ValueError("Currency count must be non-negative")
        return value

    @validator('account_page_id')
    def validate_account_page_id(cls, value):
        if value is None:
            raise ValueError("Account page ID must not be None")
        return value


