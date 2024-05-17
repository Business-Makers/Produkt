from fastapi.testclient import TestClient
from main import app
from database import SessionLocal, engine
from models import Member, Account
from schemas import Member as MemberSchema, Account as AccountSchema
from hashing import get_hashed_password
from datetime import date
import uvicorn

client = TestClient(app)


def test_register_user():
    # Testdaten
    test_member = MemberSchema(
        firstname="John",
        lastname="Doe",
        birthday=date(1990, 1, 1),
        eMail="john@example.com",
        phone_number="1234567890"
    )
    test_account = AccountSchema(
        login_name="john_doe",
        hashed_passwort="12345"
    )

    # Registrierungstest
    response = client.post("/register/", json={"member": test_member.dict(), "account": test_account.dict()})
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "member_id" in data

    return data["member_id"]


def test_login():
    # Testdaten
    test_login_name = "john_doe"
    test_password = "testpassword"
    hashed_password = get_hashed_password(test_password)

    # Benutzer erstellen
    db = SessionLocal()
    new_member = Member(firstname="John", lastname="Doe", birthday=date(1990, 1, 1),
                        eMail="john@example.com", phone_number="1234567890")
    db.add(new_member)
    db.commit()

    new_account = Account(login_name=test_login_name, hashed_password=hashed_password, memberID=new_member.member_id)
    db.add(new_account)
    db.commit()

    # Anmeldetest
    response = client.post("/login/", data={"login_name": test_login_name, "password": test_password})
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "token_type" in data


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
    # Datenbank initialisieren
    Member.metadata.create_all(bind=engine)
    Account.metadata.create_all(bind=engine)

    # Testen der Registrierungsfunktion
    member_id = test_register_user()

    # Testen der Anmeldefunktion
    test_login()