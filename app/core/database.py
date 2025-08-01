from app.config import settings
from sqlalchemy import create_engine 
from sqlalchemy.ext.declarative import declarative_base 
from sqlalchemy.orm import sessionmaker, Session 
from app.config import settings 
from app.core.exceptions import handle_database_error
from psycopg2 import DatabaseError
import logging
from typing import Generator 

logger = logging.getLogger(__name__) 

DB_URL = f"postgresql://{settings.DB_USER}:{settings.DB_PASS}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"

# Create engine for database connection
engine = create_engine(
    DB_URL, 
    pool_pre_ping=True,
    pool_recycle=300,
    echo=False,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) 

Base = declarative_base()

def get_db() -> Generator[Session, None, None]:
    """Dependency to get database session"""
    db = SessionLocal()
    try:
        yield db 
    except DatabaseError as e:
        handle_database_error(e, "grabbing database session")
        db.rollback()
        raise 
    finally:
        db.close()