from fastapi import APIRouter, HTTPException, Depends 
from core.database import get_db_connection
from core.schemas import MatchesSchema

def get_db_cursor():
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        yield cursor 
    finally:
        cursor.close()
        conn.close() 
        
router = APIRouter(prefix="matches", tags=["Matches"])

router.get("/", response_model=MatchesSchema)
async def get_matches():
    return {"message": "matches for today"}