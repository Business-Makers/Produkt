from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

engine = create_engine("sqlite:///mydb.db", echo=True)
Base.metadata.create_all(bind=engine)  # all classes extend from Base, create to database

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)  # create a class Session
