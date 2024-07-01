"""
Utils File

This file contains utility functions and variables used throughout the application.
"""
import os

import bcrypt
from datetime import timedelta, datetime
from jose import jwt, JWTError
from typing import Optional
from fastapi.security import OAuth2PasswordBearer
from fastapi import HTTPException, status
from enum import Enum, auto
from sqlalchemy.orm import Session
from models import Account, Member, Api
import mailText
import smtp_infos
from dotenv import load_dotenv
import logging
logging.basicConfig(filename='trade_debug.log', level=logging.WARNING, format='%(asctime)s %(levelname)s:%(message)s')
logger = logging.getLogger(__name__)

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 20
RESET_TOKEN_EXPIRE_MINUTES = 10
TRADE_TOKEN_EXPIRE_MINUTES = 15

dotenv_path = os.path.join(os.path.dirname(__file__),'sk.env')
load_dotenv(dotenv_path)

SECRET_KEY = os.getenv("SECRET_KEY")
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


def create_access_token(data: dict):
    """
    Creates a JWT access token.

    Parameters:
        - data (dict): The data payload to be encoded into the token.
        - expires_delta (timedelta, optional): The expiration time delta for the token (default: 15 minutes).

    Returns:
        str: The encoded JWT access token.
    """

    if not SECRET_KEY:

        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="No SECRET_KEY provided")

    expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=15)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def verify_access_token(token: str):
    """
        Verify and decode the given JWT access token.

        This function takes a JWT access token, verifies its signature, and decodes it using a secret key and the specified algorithm.
        If the token is valid, it returns the decoded payload. If the token is invalid, it returns None.

        Args:
            token (str): The JWT access token to be verified and decoded.

        Returns:
            dict or None: The decoded payload if the token is valid, otherwise None.

        Raises:
            JWTError: If there is an error in decoding or verifying the token.
        """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None


def create_trade_token(account_id):
    """
    Creates a JWT trade token.

    Parameters:
        - account_id the id from the yccount the trade will start with

    Returns:
        str: The encoded JWT tarde token.
    """
    expires_delta = timedelta(minutes=TRADE_TOKEN_EXPIRE_MINUTES)
    to_encode = account_id.copy()
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_trade_token(token: str):
    """
        Verify and decode the given JWT trade token.

        This function takes a JWT trade token, verifies its signature, and decodes it using a secret key and the specified algorithm.
        If the token is valid, it returns the decoded payload. If the token is invalid, it returns None.

        Args:
            token (str): The JWT trade token to be verified and decoded.

        Returns:
            dict or None: The decoded payload if the token is valid, otherwise None.

        Raises:
            JWTError: If there is an error in decoding or verifying the token.
        """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None


def get_current_user(token: str):
    """
        Retrieve the current user from the given JWT access token.

        This function verifies the provided JWT access token and retrieves the user information from the decoded payload.
        If the token is invalid, it raises an HTTP 401 Unauthorized exception.

        Args:
            token (str): The JWT access token to be verified and decoded.

        Returns:
            dict: The decoded payload containing user information if the token is valid.

        Raises:
            HTTPException: If the token is invalid, an HTTP 401 Unauthorized exception is raised with appropriate headers.
        """
    payload = verify_access_token(token)
    if payload is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid credentials",
                            headers={"WWW-Authenticate": "Bearer"}, )
    return payload


def generate_reset_token(username: str) -> str:
    """
    Generates a reset token for the given username.
    """
    payload = {
        "sub": username,
        "exp": datetime.now() + timedelta(minutes=RESET_TOKEN_EXPIRE_MINUTES)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def verify_reset_token(token: str) -> Optional[str]:
    """
    Verifies the reset token and returns the username if the token is valid.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        return username
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=400, detail="Expired token")
    except jwt.JWTError:
        raise HTTPException(status_code=400, detail="Invalid token")


def send_password_reset_email(email: str, token: str):
    """
    Sends a password reset email to the specified email address.
    Here you would implement your email sending logic to send the email.
    """
    # TODO Implementiere hier deine E-Mail-Versand-Logik
    pass


class mailTheme(Enum):
    """
        Enum representing the different themes for mail subjects.

        Attributes:
            login: Represents the login mail theme.
            registration: Represents the registration mail theme.
        """
    login = auto()
    registration = auto()


def find_mail(db_user, db: Session):
    """
        Find the email address associated with a given user in the database.

        This function queries the database to find the email address of a user based on their login name.
        If the email address is found, it is returned. If not, an HTTP 404 exception is raised.

        Args:
            db_user: The user object containing login information.
            db (Session): The database session to use for querying.

        Returns:
            str: The email address of the user if found.

        Raises:
            HTTPException: If the email address is not found (404) or if there is a database connection error (500).
        """
    try:
        account = db.query(Account).filter(Account.login_name == db_user.login_name).first()
        accMemberID = account.memberID
        member = db.query(Member).filter(Member.member_id == accMemberID).first()
        memberMail = member.email
        if memberMail:
            return memberMail
        else:
            raise HTTPException(status_code=404, detail="Mail not found.")

    except Exception as e:
        raise HTTPException(status_code=500, detail="DB connection failed.")


def get_name_from_mail(email, db: Session):
    """
        Retrieve the first name of a user based on their email address.

        This function queries the database to find a user's first name using their email address.
        If the user is found, their first name is returned. If not, an HTTP 404 exception is raised.

        Args:
            email (str): The email address to search for.
            db (Session): The database session to use for querying.

        Returns:
            str: The first name of the user if found.

        Raises:
            HTTPException: If the user is not found (404).
        """
    try:
        member = db.query(Member).filter(Member.email == email).first()
        if member:
            return member.firstname
    except Exception as e:
        raise HTTPException(status_code=404, detail="User name not found")


def getMailText(receiverMail, subject, db: Session):
    """
        Generate the text content for an email based on the subject and receiver's email.

        This function generates the email text content by replacing placeholders with actual values such as date, time,
        receiver's name, and support contact information. The content varies based on the subject provided.

        Args:
            receiverMail (str): The email address of the receiver.
            subject (str): The subject of the email, which determines the template to use.
            db (Session): The database session to use for querying user information.

        Returns:
            str: The generated email text content.

        Raises:
            HTTPException: If the user's name is not found.
        """
    if subject == mailTheme.login.name:
        text = mailText.loginText
        dateMail = datetime.today()
        timeMail = datetime.now()
        text = text.replace("[date]", str(dateMail))
        text = text.replace("[time]", str(timeMail))
    elif subject == mailTheme.registration.name:
        text = mailText.registrationText
    else:
        text = "No correct subject found."
    name = get_name_from_mail(receiverMail, db)
    text = text.replace("[name]", name)
    text = text.replace("[support]", smtp_infos.username_support)
    return text


def get_api_credentials(account_id: int, exchange_name: str, db: Session):
    """
        Retrieves API credentials for a specific account and exchange from the database.

        Args:
            account_id (int): The ID of the account for which API credentials are requested.
            exchange_name (str): The name of the cryptocurrency exchange.
            db (Session): The SQLAlchemy database session.

        Returns:
            dict: A dictionary containing API credentials:
                - "api_key" (str): The API key for the specified exchange and account.
                - "secret" (str): The secret key for the specified exchange and account.
                - "passphrase" (str, optional): The passphrase for the specified exchange and account, if available.

        Raises:
            ValueError: If no API credentials are found for the specified account and exchange.
        """
    api_data = db.query(Api).filter(Api.accountID == account_id, Api.exchange_name == exchange_name).first()
    if api_data:
        return {
            "api_key": api_data.key,
            "secret": api_data.secret_Key,
            "passphrase": api_data.passphrase
        }
    else:
        raise ValueError(f"No API credentials found for user {account_id} and exchange {exchange_name}")
