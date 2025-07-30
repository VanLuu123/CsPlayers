from fastapi import APIRouter, Depends
from app.core.database import get_db_connection
from app.core.schemas import MatchesSchema
from sqlalchemy.orm import Session
from app.core.models import Matches
from app.core.exceptions import handle_database_error
from psycopg2 import DatabaseError


def get_db_cursor():
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        yield cursor 
    finally:
        cursor.close()
        conn.close() 
        
router = APIRouter(prefix="/matches", tags=["Matches"])

@router.get("/", response_model=list[MatchesSchema])
async def get_matches(db: Session = Depends(get_db_cursor)):
    try:
        matches = db.query(Matches).all()
        return matches 
    except DatabaseError as e:
        handle_database_error(e, "fetching all matches")