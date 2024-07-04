import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import IntegrityError
from datetime import date
import unittest
from pydantic import ValidationError
from datetime import datetime


from models import Base, Member, Account, Login, Balance, Api, Trade, TakeProfit, Membership, Abo, \
    Subscription
from schemas import LoginCredentials, Token, TokenData, UserRegistration, PasswordResetRequest, ApiKeyCreation, AcoountPages_Info_Validate, TradeSchema, OrderRequest, AddTakeProfitStopLossRequest,UpdateTradeRequest, Subscription_Info, SellRequest



# Use an SQLite in-memory database for testing
@pytest.fixture(scope='module')
def engine():
    return create_engine('sqlite:///:memory:')


@pytest.fixture(scope='module')
def tables(engine):
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)


@pytest.fixture(scope='function')
def dbsession(engine, tables):
    connection = engine.connect()
    transaction = connection.begin()
    Session = sessionmaker(bind=connection)
    session = Session()
    yield session
    session.close()
    transaction.rollback()
    connection.close()


def test_create_member(dbsession):
    member = Member(
        firstname="John",
        lastname="Doe",
        birthday="1990-01-01",
        email="john.doe@example.com",
        phone_number="1234567890",
        address="123 Main St",
        country="USA"
    )
    dbsession.add(member)
    dbsession.commit()
    assert member.member_id is not None


def test_unique_email_constraint(dbsession):
    member1 = Member(
        firstname="Jane",
        lastname="Doe",
        birthday="1990-02-01",
        email="jane.doe@example.com",
        phone_number="1234567891",
        address="123 Main St",
        country="USA"
    )
    member2 = Member(
        firstname="Jake",
        lastname="Doe",
        birthday="1990-03-01",
        email="jane.doe@example.com",
        phone_number="1234567892",
        address="124 Main St",
        country="USA"
    )
    dbsession.add(member1)
    dbsession.commit()
    dbsession.add(member2)
    with pytest.raises(IntegrityError):
        dbsession.commit()


def test_create_account(dbsession):
    account = Account(
        login_name="alice_smith",
        hashed_password="hashed_password",
        memberID=1
    )
    dbsession.add(account)
    dbsession.commit()
    assert account.account_id is not None


def test_relationship_account_member(dbsession):
    member = Member(
        firstname="Alice",
        lastname="Smith",
        birthday="1991-01-01",
        email="alice.smith@example.com",
        phone_number="9876543210",
        address="456 Elm St",
        country="USA"
    )
    account = Account(
        login_name="alice_smith",
        hashed_password="hashed_password",
        memberID=1
    )
    dbsession.add(member)
    dbsession.add(account)
    dbsession.commit()
    assert account.account_id is not None
    assert account.memberID == member.member_id


def test_create_login(dbsession):
    login = Login(
        login_date=date.today(),
        login_time="12:00 PM",
        location="New York",
        accountID=1
    )
    dbsession.add(login)
    dbsession.commit()
    assert login.login_date is not None


def test_create_balance(dbsession):
    balance = Balance(
        balance_date=date.today(),
        balance_volume=1000.0,
        memberID=1
    )
    dbsession.add(balance)
    dbsession.commit()
    assert balance.balance_date is not None


def test_create_api(dbsession):
    api = Api(
        exchange_name="TestExchange",
        key="apikey",
        secret_Key="secretkey",
        passphrase="passphrase",
        accountID=1
    )
    dbsession.add(api)
    dbsession.commit()
    assert api.api_id is not None


def test_create_trade(dbsession):
    trade = Trade(
        trade_price=100.0,
        trade_type="buy",
        currency_name="BTC",
        currency_volume=1.0,
        trade_status="open",
        date_create=date.today(),
        api_id=1
    )
    dbsession.add(trade)
    dbsession.commit()
    assert trade.trade_id is not None


def test_create_take_profit(dbsession):
    trade = Trade(
        trade_price=100.0,
        trade_type="buy",
        currency_name="BTC",
        currency_volume=1.0,
        trade_status="open",
        date_create=date.today(),
        api_id=1
    )
    dbsession.add(trade)
    dbsession.commit()

    take_profit = TakeProfit(
        trade_id=trade.trade_id,
        price=110.0
    )
    dbsession.add(take_profit)
    dbsession.commit()
    assert take_profit.takeprofit_id is not None


def test_create_membership(dbsession):
    membership = Membership(
        membership_name="Gold",
        duration=30,
        trade_unlimited=True,
        bot_unlimited=False,
        trade_count=None,
        bot_count=None,
        price=99.99,
        price_currency="USD"
    )
    dbsession.add(membership)
    dbsession.commit()
    assert membership.membership_name is not None


def test_create_abo(dbsession):
    abo = Abo(
        abo_start=date.today(),
        abo_end=date.today(),
        abo_status="active",
        accountID=1
    )
    dbsession.add(abo)
    dbsession.commit()
    assert abo.abo_start is not None


def test_create_subscription(dbsession):
    subscription = Subscription(
        amount=100.0,
        date_start=date.today(),
        date_end=date.today(),
        product_name="Premium Subscription",
        abo_status="active",
        currency="USD",
        account_id=1,
        payment_id="payment_12345"
    )
    dbsession.add(subscription)
    dbsession.commit()
    assert subscription.subscription_id is not None


def test_login_credentials_valid():
    data = {"login_name": "testuser", "password": "testpassword"}
    model = LoginCredentials(**data)
    assert model.login_name == "testuser"
    assert model.password == "testpassword"

def test_login_credentials_invalid():
    data = {"login_name": "testuser"}
    try:
        LoginCredentials(**data)
    except ValidationError:
        assert True
    else:
        assert False

def test_token_valid():
    data = {"access_token": "1234567890", "token_type": "bearer"}
    model = Token(**data)
    assert model.access_token == "1234567890"
    assert model.token_type == "bearer"

def test_token_invalid():
    data = {"access_token": "short", "token_type": "bearer"}
    try:
        Token(**data)
    except ValidationError:
        assert True
    else:
        assert False

def test_user_registration_valid():
    data = {
        "firstname": "John",
        "lastname": "Doe",
        "birthday": "2000-01-01",
        "eMail": "john.doe@example.com",
        "login_name": "johndoe",
        "password": "Password123"
    }
    model = UserRegistration(**data)
    assert model.firstname == "John"
    assert model.lastname == "Doe"

def test_user_registration_invalid_email():
    data = {
        "firstname": "John",
        "lastname": "Doe",
        "birthday": "2000-01-01",
        "eMail": "not-an-email",
        "login_name": "johndoe",
        "password": "Password123"
    }
    try:
        UserRegistration(**data)
    except ValidationError:
        assert True
    else:
        assert False

def test_trade_schema_invalid():
    data = {
        "trade_type": "buy",
        "currency_name": "BTC",
        "currency_volume": -1.5,
        "trade_status": "open",
        "date_create": datetime.now()
    }
    try:
        TradeSchema(**data)
    except ValidationError:
        assert True
    else:
        assert False

def test_order_request_valid():
    data = {
        "trade_price": 100.0,
        "symbol": "BTC/USD",
        "side": "buy",
        "amount": 1.0,
        "order_type": "market",
        "exchangeName": "binance"
    }
    model = OrderRequest(**data)
    assert model.trade_price == 100.0
    assert model.symbol == "BTC/USD"

def test_order_request_invalid():
    data = {
        "trade_price": 100.0,
        "symbol": "BTC/USD",
        "side": "buy",
        "amount": 1.0
    }
    try:
        OrderRequest(**data)
    except ValidationError:
        assert True
    else:
        assert False


