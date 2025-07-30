from fastapi import APIRouter, Depends 
from app.core.database import get_db_connection 
from app.core.schemas import PlayerSchema 
from sqlalchemy.orm import Session
from app.core.models import CsPlayers
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
        
router = APIRouter(prefix="/players", tags=["Players"])


# Return List of all players
@router.get("/", response_model=list[PlayerSchema]) 
async def get_players(db: Session = Depends(get_db_cursor)):
    try:
        players = db.query(CsPlayers).all()
        return players
    except DatabaseError as e:
        handle_database_error(e, "fetching all players")

@router.get("/{player_name}", response_model=PlayerSchema)
async def get_player(player_name: str, db: Session = Depends(get_db_cursor)):
    try:
        player = db.query(CsPlayers).filter(CsPlayers.name == player_name).first()
        if not player:
            print(f"Player {player_name} not found")
        return player
    except DatabaseError as e:
        handle_database_error(e, "fetching player")
    
    
    