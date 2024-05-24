"""
FastAPI Application File

This file contains the main FastAPI application setup, including endpoint definitions and event handlers.
"""

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import timedelta

from database import get_db, init_db
from models import Account, Member
from schemas import LoginCredentials, UserRegistration, Token
from utils import get_hashed_password, verify_password, create_access_token

app = FastAPI()  # creates instance of FastAPI class


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
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        # Generate token
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": db_user.login_name}, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}

    if db_user and verify_password(credentials.password, db_user.hashed_password):
        return {"message": "Logged in successfully"}
    else:
        raise HTTPException(status_code=400, detail="Incorrect username or password")


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
        dict: A dictionary containing the success message if registration is successful.
    """
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
            memberID=new_member.member_id  # Link the account to the member via foreign key
        )
        db.add(new_account)
        db.commit()



    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
