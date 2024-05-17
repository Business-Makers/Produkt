from fastapi import FastAPI, Depends, HTTPException
from database import SessionLocal
from models import Member, Account
from hashing import *
from schemas import *
app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/register/", status_code=status.HTTP_201_CREATED)
def register_user(user_data: UserRegistration, db: Session = Depends(get_db)):
    # Überprüfe, ob die E-Mail oder der Benutzername bereits registriert ist
    existing_member = db.query(Member).filter(Member.eMail == user_data.email).first()
    existing_account = db.query(Account).filter(Account.login_name == user_data.login_name).first()
    if existing_member:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    if existing_account:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already taken")

    # Erstelle neuen Member
    new_member = Member(
        firstname=user_data.firstname,
        lastname=user_data.lastname,
        birthday=user_data.birthday,
        eMail=user_data.email,
        phone_number=user_data.phone_number,
        address=user_data.address,
        country=user_data.country
    )
    db.add(new_member)
    db.flush()  # Um die member_id zu erhalten, nachdem sie zugewiesen wurde

    # Hashed das Passwort
    hashed_password = get_hashed_password(user_data.password)

    # Erstelle neuen Account
    new_account = Account(
        login_name=user_data.login_name,
        hashed_password=hashed_password,
        memberID=new_member.member_id
    )
    db.add(new_account)

    try:
        db.commit()
        return {"message": "Registration successful", "member_id": new_member.member_id}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/login/")
def login(login_name: str, password: str, db: Session = Depends(get_db)):
    user = authenticate_user(db, login_name, password)
    token = create_access_token({"sub": user.login_name})
    return {"access_token": token, "token_type": "bearer"}


# Weitere Endpunkte.

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
