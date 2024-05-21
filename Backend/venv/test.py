import pytest
from fastapi.testclient import TestClient
from database import SessionLocal, engine, Base
from main import app, get_db
from hashing import get_hashed_password, verify_password, authenticate_user
from models import Account, Member
from sqlalchemy.orm import Session
from schemas import Member, UserRegistration
from datetime import date


def override_get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="module")
def test_app():
    client = TestClient(app)
    yield client
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

@pytest.fixture(scope="module")
def db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

def test_get_hashed_password():
    password = "mysecretpassword"
    hashed = get_hashed_password(password)
    assert hashed != password

def test_verify_password():
    password = "mysecretpassword"
    hashed = get_hashed_password(password)
    assert verify_password(password, hashed)
    assert not verify_password("wrongpassword", hashed)

def test_authenticate_user(db: Session):
    member = Member(firstname="John", lastname="Doe", birthday="1990-01-01", eMail="john@example.com", phone_number="1234567890", address="123 Street", country="Country")
    db.add(member)
    db.flush()
    account = Account(login_name="johndoe", hashed_password=get_hashed_password("mypassword"), memberID=member.member_id)
    db.add(account)
    db.commit()

    user = authenticate_user(db, "johndoe", "mypassword")
    assert user is not None
    assert user.login_name == "johndoe"

    user = authenticate_user(db, "johndoe", "wrongpassword")
    assert user is None

def test_register_user(test_app):
    response = test_app.post("/register/", json={
        "firstname": "Jane",
        "lastname": "Doe",
        "birthday": "1990-01-01",
        "email": "jane@example.com",
        "phone_number": "1234567890",
        "address": "123 Street",
        "country": "Country",
        "login_name": "janedoe",
        "password": "mypassword"
    })
    assert response.status_code == 200
    assert response.json()["message"] == "Registration successful"

def test_register_user_existing_email(test_app):
    response = test_app.post("/register/", json={
        "firstname": "John",
        "lastname": "Smith",
        "birthday": "1990-01-01",
        "email": "jane@example.com",
        "phone_number": "1234567890",
        "address": "123 Street",
        "country": "Country",
        "login_name": "johnsmith",
        "password": "mypassword"
    })
    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"

def test_login(test_app):
    response = test_app.post("/login/", json={
        "login_name": "janedoe",
        "password": "mypassword"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()

# Test für models.py
def test_member_model():
    member = Member(firstname="John", lastname="Doe", birthday="1990-01-01", eMail="john@example.com", phone_number="1234567890")
    assert member.firstname == "John"
    assert member.lastname == "Doe"
    assert member.birthday == "1990-01-01"
    assert member.eMail == "john@example.com"
    assert member.phone_number == "1234567890"

# Test für schemas.py
def test_member_create_schema():
    schema = UserRegistration(firstname="John", lastname="Doe", birthday="1990-01-01", eMail="john@example.com", phone_number="1234567890")
    assert schema.firstname == "John"
    assert schema.lastname == "Doe"
    assert schema.birthday == "1990-01-01"
    assert schema.eMail == "john@example.com"
    assert schema.phone_number == "1234567890"

def test_member_update_schema():
    schema = Member(firstname="Jane", lastname="Doe", birthday="1990-01-01", eMail="jane@example.com", phone_number="1234567890")
    assert schema.firstname == "Jane"
    assert schema.lastname == "Doe"
    assert schema.birthday == "1990-01-01"
    assert schema.eMail == "jane@example.com"
    assert schema.phone_number == "1234567890"

def test_member_model_valid():
    data = {
        "firstname": "John",
        "lastname": "Doe",
        "birthday": "1990-01-01",
        "email": "john@example.com",
        "phone_number": "1234567890",
        "address": "123 Street",
        "country": "Country"
    }
    member = Member(**data)
    assert member.firstname == "John"
    assert member.lastname == "Doe"
    assert member.birthday == date(1990, 1, 1)
    assert member.eMail == "john@example.com"
    assert member.phone_number == "1234567890"
    assert member.address == "123 Street"
    assert member.country == "Country"

def test_member_model_invalid_phone_number():
    data = {
        "firstname": "John",
        "lastname": "Doe",
        "birthday": "1990-01-01",
        "email": "john@example.com",
        "phone_number": "abc123",
        "address": "123 Street",
        "country": "Country"
    }
    try:
        member = Member(**data)
    except ValueError as e:
        assert "Phone number must contain only digits" in str(e)

def test_member_model_invalid_age():
    data = {
        "firstname": "John",
        "lastname": "Doe",
        "birthday": "2022-01-01",  # Assuming today's date is 2024-05-21
        "email": "john@example.com",
        "phone_number": "1234567890",
        "address": "123 Street",
        "country": "Country"
    }
    try:
        member = Member(**data)
    except ValueError as e:
        assert "Member must be at least 18 years old" in str(e)
