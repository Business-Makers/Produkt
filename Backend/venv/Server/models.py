from sqlalchemy import create_engine, Column, Integer, String, DATE, Float, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()
engine = create_engine("sqlite:///./Database.db")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Member(Base):
    __tablename__ = 'member'
    member_id = Column(Integer, primary_key=True, autoincrement=True)
    firstname = Column(String(50), nullable=False)
    lastname = Column(String(50), nullable=False)
    birthday = Column(String(50), nullable=False)
    email = Column(String(50), unique=True, nullable=False)
    phone_number = Column(String(50), unique=True)
    address = Column(String(50))
    country = Column(String(50))
    accounts = relationship("Account", back_populates="member")

class Account(Base):
    __tablename__ = 'account'
    account_id = Column(Integer, primary_key=True, autoincrement=True)
    login_name = Column(String(50), nullable=False, unique=True)
    hashed_password = Column(String(255), nullable=False)
    member_id = Column(Integer, ForeignKey('member.member_id'))
    member = relationship("Member", back_populates="accounts")

# Add other models as per your initial code with similar structure adjustments

Base.metadata.create_all(bind=engine)
