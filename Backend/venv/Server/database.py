from datetime import timedelta, datetime
from fastapi.security import OAuth2PasswordBearer
from jose import jwt

"""
This module configures and initializes a database using SQLAlchemy ORM. It sets up an SQLite database, creates tables based on defined models, and configures a session factory for database operations.

Details:
- Uses SQLite as the database engine.
- Echoes SQL commands to the standard output to help with debugging.
- Disables both autocommit and autoflush to give more control over transactions.
"""
from fastapi import HTTPException
import uvicorn
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional

"""
This module defines the database schema for a system that manages members, accounts, and various transactions.
It uses SQLAlchemy's ORM capabilities to map Python classes to database tables. The following entities are
defined:

- Member: Stores information about members including personal details and contact information.
- Account: Contains login and authentication information for each member.
- Login: Tracks login activities by date, time, and location for accounts.
- Balance: Manages financial balances with dates and volumes linked to members.
- AccountPages: Stores API access configurations for third-party services, including credentials.
- Trade: Tracks currency trades, including details like volume, status, rates, and associated member.
- Membership: Defines different membership types available, detailing features and pricing.
- Abo: Manages subscription details for accounts including start and end dates and the status of the subscription.

Each class maps to a specific table in the database and includes primary keys, foreign keys, and necessary constraints
to ensure data integrity. Relationships between tables are established through foreign keys, enabling connected data
operations across the system.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from sqlalchemy import ForeignKey, Column, String, Integer, DATE, Float, Boolean
import bcrypt

# basic class used for table definition
Base = declarative_base()


class Member(Base):
    """
    This class defines the database schema for a system that manages members.
    It stores the personal details and contact information for each member.
    """
    __tablename__ = 'member'
    member_id = Column("member_id", Integer, unique=True, primary_key=True, autoincrement=True)
    firstname = Column("firstname", String(50), nullable=False)
    lastname = Column("lastname", String(50), nullable=False)
    birthday = Column("birthday", String(50), nullable=False)
    address = Column("address", String(50))
    country = Column("country", String(50))
    email = Column("email", String(50), unique=True, nullable=False)
    phone_number = Column("phone_number", String(50), unique=True)
    accounts = relationship("Account", back_populates="member")

    def __init__(self, firstname, lastname, birthday, email, phone_number, address=None, country=None):
        self.firstname = firstname
        self.lastname = lastname
        self.birthday = birthday
        self.address = address
        self.country = country
        self.email = email
        self.phone_number = phone_number


class Account(Base):
    """
    stores the Login and authentication information for each member.
    """
    __tablename__ = 'account'
    account_id = Column("account_id", Integer, primary_key=True, unique=True, autoincrement=True)
    login_name = Column("login_name", String(50), nullable=False, unique=True)
    hashed_password = Column("hashed_password", String(50), nullable=False)
    memberID = Column("memberID", Integer, ForeignKey("member.member_id"), nullable=False)
    # TODO:
    member = relationship("Member", back_populates="accounts")

    def __init__(self, login_name, hashed_password, memberID):
        self.login_name = login_name
        self.hashed_password = hashed_password
        self.memberID = memberID


class Login(Base):
    """
    tracks login activities by date, time, and location for accounts.
    """
    __tablename__ = 'login'
    login_date = Column("login_date", DATE, primary_key=True)
    login_time = Column("login_time", String(50), nullable=False)
    location = Column("location", String(50), nullable=False)
    accountID = Column("accountID", Integer, ForeignKey("account.account_id"), primary_key=True, nullable=False)

    def __init__(self, login_date, login_time, location, accountID):
        self.login_date = login_date
        self.login_time = login_time
        self.location = location
        self.accountID = accountID


class Balance(Base):
    """stores the daily balance for each account."""
    __tablename__ = 'balance'
    balance_date = Column("balance_date", DATE, nullable=False, primary_key=True)
    balance_volume = Column("balance_volume", Float, nullable=False)
    memberID = Column("memberID", Integer, ForeignKey("member.member_id"), primary_key=True, nullable=False)

    def __init__(self, balance_date, balance_volume, memberID):
        self.balance_date = balance_date
        self.balance_volume = balance_volume
        self.memberID = memberID


class AccountPages(Base):
    """
    stores API access configurations for third-party services, including credentials.
    """
    __tablename__ = 'account_pages'
    ap_id = Column("ap_id", Integer, primary_key=True, unique=True, autoincrement=True)
    api_name = Column("api_name", String(50), nullable=False)
    key = Column("key", String(50), nullable=False)
    secret_Key = Column("secret_key", String(50), nullable=False, unique=True)
    passphrase = Column("passphrase", String(50), nullable=False)
    stock = Column("stock", String(50), nullable=False)
    user_name = Column("user_name", String(50), nullable=False)
    ap_value = Column("ap_value", String(50))
    memberID = Column("memberID", Integer, ForeignKey("member.member_id"), nullable=False)

    def __init__(self, api_name, key, secret_Key, passphrase, stock, user_name, ap_value, memberID):
        self.api_name = api_name
        self.key = key
        self.secret_Key = secret_Key
        self.passphrase = passphrase
        self.stock = stock
        self.user_name = user_name
        self.ap_value = ap_value
        self.memberID = memberID


class Trade(Base):
    """
    stores all Trades, including details like currency, volume, status, rates
    """
    __tablename__ = 'trade'
    trade_id = Column("trade_id", Integer, primary_key=True, unique=True, autoincrement=True)
    currency_name = Column("currency_name", String(50), nullable=False)
    currency_volume = Column("currency_volume", Float, nullable=False)
    trade_status = Column("trade_status", String(50))
    date_create = Column("date_create", DATE, nullable=False)
    date_bought = Column("date_bought", DATE)
    date_sale = Column("date_sale", DATE)
    purchase_rate = Column("purchase_rate", Float)
    selling_rate = Column("selling_rate", Float)
    comment = Column("comment", String(50))
    memberID = Column("memberID", Integer, ForeignKey("member.member_id"), nullable=False)

    def __init__(self, currency_name, currency_volume, trade_status, date_create, memberID, date_bought=None,
                 date_sale=None, purchase_rate=None, selling_rate=None, comment=None):
        self.currency_name = currency_name
        self.currency_volume = currency_volume
        self.trade_status = trade_status
        self.date_create = date_create
        self.memberID = memberID
        self.date_bought = date_bought
        self.date_sale = date_sale
        self.purchase_rate = purchase_rate
        self.selling_rate = selling_rate
        self.comment = comment


class Membership(Base):
    """
    Defines different types of memberships, detailing features and differences.
    """
    __tablename__ = 'membership'
    membership_name = Column("membership_name", String, primary_key=True, unique=True)
    duration = Column('duration', Integer, nullable=False)
    trade_unlimited = Column("trade_unlimited", Boolean, nullable=False)
    bot_unlimited = Column("bot_unlimited", Boolean, nullable=False)
    trade_count = Column("trade_count", Integer)
    bot_count = Column("bot_count", Integer)
    price = Column("price", Float, nullable=False)
    price_currency = Column("price_currency", String(50), nullable=False)

    def __init__(self, membership_name, duration, trade_unlimited, bot_unlimited, trade_count, bot_count, price,
                 price_currency):
        self.membership_name = membership_name
        self.duration = duration
        self.trade_unlimited = trade_unlimited
        self.bot_unlimited = bot_unlimited
        self.trade_count = trade_count
        self.bot_count = bot_count
        self.price = price
        self.price_currency = price_currency


class Abo(Base):
    """
        Manages subscription details for accounts including start and end dates and the status of the subscription.
        """
    __tablename__ = 'abo'
    abo_start = Column('abo_start', DATE, primary_key=True)
    abo_end = Column('abo_end', DATE)
    abo_status = Column('abso_status', String, nullable=False)
    accountID = Column('accountID', Integer, ForeignKey("account.account_id"), primary_key=True)

    def __init__(self, abo_start, abo_end, abo_status, accountID):
        self.abo_start = abo_start
        self.abo_end = abo_end
        self.abo_status = abo_status
        self.accountID = accountID


# create SQLite database and tables
engine = create_engine("sqlite:///Database.db", echo=True)
Base.metadata.create_all(bind=engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = SessionLocal()

session.close()  # close the initial session

app = FastAPI()  # creates instance of FastAPI class


def get_db():
    """
    Dependency that provides a database session to endpoints.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class LoginCredentials(BaseModel):
    """
    model for login credentials.
    """
    login_name: str
    password: str


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


class Token(BaseModel):
    """
    Model for an access token.
    """
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """
    Model for token data.
    """
    username: Optional[str] = None


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    creates an JWT access token
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


class UserRegistration(BaseModel):
    """
    Model for user registration details.
    """
    firstname: str
    lastname: str
    birthday: str
    eMail: str
    phone_number: Optional[str] = None
    address: Optional[str] = None
    country: Optional[str] = None
    login_name: str
    password: str


def get_hashed_password(password: str) -> str:
    """
    Hashes a password with bcrypt.
    """
    password_bytes = password.encode('utf-8')
    hashed = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
    return hashed.decode('utf-8')


def verify_password(plain_password: str, hashed_password_from_db: str) -> bool:
    """
       Verify a plain password against a hashed password.
       """
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password_from_db.encode('utf-8'))


# word = "hashed_pwd123"
# newPasswort = get_hashed_password(word)
# print(newPasswort)
# new_user = Account(login_name="test_user1122", hashed_password=newPasswort, memberID=6)
# session.add(new_user)
# session.commit()


@app.post("/login/")
def login(credentials: LoginCredentials, db: Session = Depends(get_db)):
    """
    Handling user login and password.
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
    Handling new user registration.
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


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8001)
