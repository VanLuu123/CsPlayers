from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import uvicorn 
from core.database import get_db_connection
from core import schemas, models, database
from config import settings


app = FastAPI(
    title="CS Esport Players API",
    description="A simple FastApi application displaying relevant data from CS Players",
    version="1.0.0"
)

def get_db_cursor():
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        yield cursor 
    finally:
        cursor.close()
        conn.close()
    
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


#root url
@app.get("/")
async def root():
    return {"message": "Welcome to CsPlayers API!", "status": "running"}

#check health API 
@app.get("/health")
async def health_check():
    return {"status": "healthy", "service":"CS Players API"}

# Return List of all players
@app.get("/players") 
async def get_players(cursor = Depends(get_db_cursor)):
    try:
        cursor.execute(" SELECT * FROM CsPlayers ")
        players = cursor.fetchall()
        if not players:
            raise HTTPException(status_code=404, detail="Players not found")
        return {"players": players}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error finding players: {str(e)}") 

@app.get("/players/{player_name}", response_model=schemas.PlayerSchema)
async def get_player(player_name: str, cursor=Depends(get_db_cursor)):
    try:
        cursor.execute("SELECT * FROM CsPlayers WHERE name = %s", (player_name,))
        player = cursor.fetchone()
        if not player:
            raise HTTPException(status_code=404, detail="Player not found")
        return player
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error finding player: {str(e)}")

        

@app.get("/matches", response_model=schemas.MatchesSchema)
async def get_matches():
    return {"message": "matches for today"}

@app.get("/teams")
async def get_teams():
    return {"message": "All team matches"}

@app.get("/teams/{team}")
async def get_team(team: str):
    return {"message": f"Team Match History : {team}"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)