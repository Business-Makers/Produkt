"""
This module configures and initializes a database using SQLAlchemy ORM. It sets up an SQLite database, creates tables based on defined models, and configures a session factory for database operations.

Details:
- Uses SQLite as the database engine.
- Echoes SQL commands to the standard output to help with debugging.
- Disables both autocommit and autoflush to give more control over transactions.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base
import logging

logging.basicConfig(filename='debugAll.log', level=logging.WARNING, format='%(asctime)s %(levelname)s:%(message)s')
logger = logging.getLogger(__name__)

DATABASE_URL = "sqlite:///Database.db"
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    """
       Initializes the Database by creating all tables defined in the SQLAlchemy models.

       This function creates all tables in the database based on the SQLAlchemy models defined in the application.
       It uses the `Base.metadata.create_all()` method to create the tables and binds them to the database engine.
       """
    Base.metadata.create_all(bind=engine)


def get_db():
    """
    Dependency that provides a database session to endpoints.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
