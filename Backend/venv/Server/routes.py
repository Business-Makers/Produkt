"""
FastAPI Application File

This file contains the main FastAPI application setup, including endpoint definitions and event handlers.
"""

from fastapi import FastAPI, Depends, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import timedelta
import time
from database import get_db, init_db
from models import Account, Member, Api, AccountPages_Info
from schemas import LoginCredentials, UserRegistration, PasswordResetRequest, ApiKeyCreation
from utils import get_hashed_password, verify_password, create_access_token, generate_reset_token, \
    send_password_reset_email, verify_reset_token, verify_access_token, find_mail, mailTheme
from smtp import send_email
from ExchangeConnection import get_balance_and_currency_count
import ccxt

app = FastAPI()  # creates instance of FastAPI class

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Erlaubte Ursprünge
    allow_credentials=True,
    allow_methods=["*"],  # Erlaubte HTTP-Methoden
    allow_headers=["*"],  # Erlaubte HTTP-Header
)


@app.on_event("startup")
def on_startup():
    """
        Event handler function called on application startup.

        This function is automatically called when the FastAPI application starts up.
        It is decorated with `@app.on_event("startup")` to register it as an event handler for the application startup event.
        Inside this function, it calls the `init_db()` function to initialize the database by creating all tables.
        """
    init_db()


@app.post("/login/")
def login(credentials: LoginCredentials, db: Session = Depends(get_db)):
    """
    Handles user login and password authentication.

    This endpoint is responsible for authenticating user login credentials.
    It takes the login credentials provided by the user and checks them against the stored hashed password in the database.
    If the credentials are correct, it generates an access token and returns it to the client.

    Parameters:
        - credentials (LoginCredentials): The user's login credentials containing username and password.
        - db (Session, optional): The database session dependency obtained using `Depends(get_db)`.

    Returns:
        dict: A dictionary containing the access token and token type if authentication is successful.
    """
    try:
        db_user = db.query(Account).filter(Account.login_name == credentials.login_name).first()
        if db_user and verify_password(credentials.password, db_user.hashed_password):
            # Generate token

            access_token = create_access_token(
                data={"sub": db_user.login_name},
            )

            mailAdress = find_mail(db_user, db)
            if mailAdress:
                send_email(mailAdress, mailTheme.login.name, db)

            return {"message": "Logged in successfully", "access_token": access_token, "token_type": "bearer"}
        else:
            raise HTTPException(status_code=401, detail="Incorrect username or password")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/register/")
def register(user: UserRegistration, db: Session = Depends(get_db)):
    """
    Handles new user registration.

    This endpoint is responsible for registering new users.
    It takes the user registration details provided by the client, creates a new member and account in the database,
    and associates them together. It also hashes the user's password before storing it in the database.

    Parameters:
        - user (UserRegistration): The user's registration details containing personal information and login credentials.
        - db (Session, optional): The database session dependency obtained using `Depends(get_db)`.

    Returns:
        dict: A dictionary containing the success message if registration is successful.pass
    """
    if user.phone_number:
        existing_phone_number = db.query(Member).filter(Member.phone_number == user.phone_number).first()
        if existing_phone_number:
            raise HTTPException(status_code=400, detail="Phone number already registered")

    existing_email = db.query(Member).filter(Member.email == user.eMail).first()
    if existing_email:
        raise HTTPException(status_code=400, detail="Email already registered")

    existing_user = db.query(Account).filter(Account.login_name == user.login_name).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Login name already registered")

    try:

        new_member = Member(
            firstname=user.firstname,
            lastname=user.lastname,
            birthday=user.birthday,
            email=user.eMail,
            phone_number=user.phone_number,
            address=user.address,
            country=user.country
        )

        db.add(new_member)
        db.commit()
        db.refresh(new_member)

        hashed_password = get_hashed_password(user.password)
        new_account = Account(
            login_name=user.login_name,
            hashed_password=hashed_password,
            memberID=new_member.member_id
        )
        db.add(new_account)
        db.commit()

        send_email(user.eMail, mailTheme.registration.name, db)
        return {"message": "Registration successful! We're excited to have you with us."}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/connect-exchange/")
def connect_exchange(exchange_info: ApiKeyCreation, db: Session = Depends(get_db), authorization: str = Header(None), ):
    if authorization is None or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Authorization header missing or invalid.")

    token = authorization.split(" ")[1]
    payload = verify_access_token(token)
    if payload is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        if exchange_info.passphrase:
            exchange_class = getattr(ccxt, exchange_info.exchange_id)
            exchange = exchange_class({
                'apiKey': exchange_info.api_key,
                'secret': exchange_info.api_secret,
                'password': exchange_info.api_passphrase,
            })
        else:
            exchange_class = getattr(ccxt, exchange_info.exchange_id)
            exchange = exchange_class({
                'apiKey': exchange_info.api_key,
                'secret': exchange_info.api_secret,
            })
        try:
            new_ApiKey = Api(
                api_name=exchange_info.api_name,
                key=exchange_info.key,
                secret_Key=exchange_info.secret_key,
                passphrase=exchange_info.passphrase,
                accountID=payload.get("account_id")
            )
            db.add(new_ApiKey)
            db.commit()
            db.refresh(new_ApiKey)

            balanceofaccount, number_of_currencies = get_balance_and_currency_count(exchange)

            new_accountpages_info = AccountPages_Info(
                balance=balanceofaccount,
                currency_count=number_of_currencies,
                api_id=new_ApiKey.api_id,
            )
            db.add(new_accountpages_info)
            db.commit()
            db.close()
            return new_accountpages_info
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=str(e))

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/request-password-reset/")
def forgot_password(email: str, db: Session = Depends(get_db)):
    """
        Handles the request to reset a password.

        This endpoint sends a password reset email to the provided email address.
        It retrieves the user associated with the given email, generates a reset token,
        and sends an email with the token to the user's email address.

        Parameters:
            - email (str): The email address of the user requesting the password reset.
            - db (Session, optional): The database session dependency obtained using `Depends(get_db)`.

        Returns:
            dict: A dictionary containing a success message if the email was sent successfully.
        """
    user = db.query(Account).filter(Account.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    reset_token = generate_reset_token(user.login_name)
    send_password_reset_email(user.email, reset_token)
    return {"message": "Passwort-Reset was send to your email address."}


@app.post("/reset-password/")
def reset_password(reset_request: PasswordResetRequest, db: Session = Depends(get_db)):
    """
        Handles resetting a user's password.

        This endpoint allows users to reset their password using a valid reset token.
        It verifies the provided token, updates the user's password with the new one,
        and commits the changes to the database.

        Parameters:
            - reset_request (PasswordResetRequest): The request containing the reset token and new password.
            - db (Session, optional): The database session dependency obtained using `Depends(get_db)`.

        Returns:
            dict: A dictionary containing a success message if the password was reset successfully.
        """
    user = verify_reset_token(reset_request.token)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid token.")
    hashed_password = get_hashed_password(reset_request.new_password)
    user.hashed_password = hashed_password
    db.commit()

    return {"message": "Password reset successfully."}
