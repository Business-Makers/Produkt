import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from fastapi import FastAPI
from models import Base
from database import get_db



# Create a new database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
app = FastAPI()
# Override the get_db dependency to use the testing database
@pytest.fixture(scope="module")
def test_db():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="module")
def client():
    app.dependency_overrides[get_db] = test_db
    with TestClient(app) as c:
        yield c

@pytest.fixture
def user_registration_data():
    return {
        "firstname": "John",
        "lastname": "Doe",
        "birthday": "2000-01-01",
        "eMail": "john.doe@example.com",
        "phone_number": "1234567890",
        "address": "123 Main St",
        "country": "USA",
        "login_name": "johndoe",
        "password": "Password123"
    }

def test_register_success(client, user_registration_data):
    response = client.post("/register/", json=user_registration_data)
    assert response.status_code == 200
    assert response.json() == {"message": "Registration successful! We're excited to have you with us."}

def test_register_existing_email(client, user_registration_data):
    client.post("/register/", json=user_registration_data)  # Register first user
    response = client.post("/register/", json=user_registration_data)  # Try to register with same email
    assert response.status_code == 400
    assert response.json() == {"detail": "Email already registered"}

def test_register_existing_phone_number(client, user_registration_data):
    client.post("/register/", json=user_registration_data)  # Register first user
    new_user_data = user_registration_data.copy()
    new_user_data["eMail"] = "new.email@example.com"  # Change email to avoid conflict
    response = client.post("/register/", json=new_user_data)  # Try to register with same phone number
    assert response.status_code == 400
    assert response.json() == {"detail": "Phone number already registered"}

def test_register_existing_login_name(client, user_registration_data):
    client.post("/register/", json=user_registration_data)  # Register first user
    new_user_data = user_registration_data.copy()
    new_user_data["eMail"] = "new.email@example.com"  # Change email to avoid conflict
    new_user_data["phone_number"] = "0987654321"  # Change phone number to avoid conflict
    response = client.post("/register/", json=new_user_data)  # Try to register with same login name
    assert response.status_code == 400
    assert response.json() == {"detail": "Login name already registered"}

def test_register_invalid_password(client, user_registration_data):
    new_user_data = user_registration_data.copy()
    new_user_data["password"] = "short"  # Invalid password
    response = client.post("/register/", json=new_user_data)
    assert response.status_code == 422

def test_register_invalid_email(client, user_registration_data):
    new_user_data = user_registration_data.copy()
    new_user_data["eMail"] = "not-an-email"  # Invalid email
    response = client.post("/register/", json=new_user_data)
    assert response.status_code == 422

def test_register_invalid_login_name(client, user_registration_data):
    new_user_data = user_registration_data.copy()
    new_user_data["login_name"] = "a"  # Invalid login name
    response = client.post("/register/", json=new_user_data)
    assert response.status_code == 422
