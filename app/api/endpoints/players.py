from fastapi import APIRouter, HTTPException, Depends 
from app.core.database import get_db_connection 
from app.core.schemas import PlayerSchema 

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
async def get_players(cursor = Depends(get_db_cursor)):
    try:
        cursor.execute(" SELECT * FROM CsPlayers ")
        players = cursor.fetchall()
        if not players:
            raise HTTPException(status_code=404, detail="Players not found")
        return {"players": players}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error finding players: {str(e)}") 

@router.get("/{player_name}", response_model=PlayerSchema)
async def get_player(player_name: str, cursor=Depends(get_db_cursor)):
    try:
        cursor.execute("SELECT * FROM CsPlayers WHERE name = %s", (player_name,))
        player = cursor.fetchone()
        if not player:
            raise HTTPException(status_code=404, detail="Player not found")
        return player
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error finding player: {str(e)}")
    
    
    