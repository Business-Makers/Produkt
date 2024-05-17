from sqlalchemy import ForeignKey, Column, String, Integer, DATE, Float, Boolean
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Member(Base):
    __tablename__ = 'member'
    member_id = Column("member_id", Integer, unique=True, primary_key=True, autoincrement=True)
    firstname = Column("firstname", String(50), nullable=False)
    lastname = Column("lastname", String(50), nullable=False)
    birthday = Column("birthday", String(50), nullable=False)
    address = Column("address", String(50))
    country = Column("country", String(50))
    eMail = Column("eMail", String(50), unique=True, nullable=False)
    phone_number = Column("phone_number", String(50), unique=True)


class Account(Base):
    __tablename__ = 'account'
    account_id = Column("account_id", Integer, primary_key=True, unique=True, autoincrement=True)
    login_name = Column("login_name", String(50), nullable=False, unique=True)
    hashed_password = Column("hashed_password", String(50), nullable=False)
    memberID = Column("memberID", Integer, ForeignKey("member.member_id"), nullable=False)


class Login(Base):
    __tablename__ = 'login'
    login_date = Column("login_date", DATE, primary_key=True)
    login_time = Column("login_time", String(50), nullable=False)
    location = Column("location", String(50), nullable=False)
    accountID = Column("accountID", Integer, ForeignKey("account.account_id"), primary_key=True, nullable=False)


class Balance(Base):
    __tablename__ = 'balance'
    balance_date = Column("balance_date", DATE, nullable=False, primary_key=True)
    balance_volume = Column("balance_volume", Float, nullable=False)
    memberID = Column("memberID", Integer, ForeignKey("member.member_id"), primary_key=True, nullable=False)


class AccountPages(Base):
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


class Trade(Base):
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


class Membership(Base):
    __tablename__ = 'membership'
    membership_name = Column("membership_name", String, primary_key=True, unique=True)
    duration = Column('duration', Integer, nullable=False)
    trade_unlimited = Column("trade_unlimited", Boolean, nullable=False)
    bot_unlimited = Column("bot_unlimited", Boolean, nullable=False)
    trade_count = Column("trade_count", Integer)
    bot_count = Column("bot_count", Integer)
    price = Column("price", Float, nullable=False)
    price_currency = Column("price_currency", String(50), nullable=False)


class Abo(Base):
    __tablename__ = 'abo'
    abo_start = Column('abo_start', DATE, primary_key=True)
    abo_end = Column('abo_end', DATE)
    abo_status = Column('abso_status', String, nullable=False)
    accountID = Column('accountID', Integer, ForeignKey("account.account_id"), primary_key=True)
