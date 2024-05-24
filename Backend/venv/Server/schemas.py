"""
Pydantic Schemas File

This file contains Pydantic models representing data schemas used for validation and serialization.
"""

from pydantic import BaseModel, EmailStr
from typing import Optional


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
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """
    Model for token data.

    This Pydantic model represents the schema for token data.
    It defines the structure and data types of the username field.

    Attributes:
        - username (str, optional): The username extracted from the token data.
    """
    username: Optional[str] = None


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
    firstname: str
    lastname: str
    birthday: str
    eMail: EmailStr
    phone_number: Optional[str] = None
    address: Optional[str] = None
    country: Optional[str] = None
    login_name: str
    password: str


class PasswordResetRequest(BaseModel):
    """
        Represents a request to reset a password.

        Attributes:
            token (Token): The reset token.
            new_password (str): The new password to set.
        """
    token: Token
    new_password: str
