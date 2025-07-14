from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn 
from core.database import get_db_connection


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
    
origin = "http://0.0.0.0:8000/"

app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin],
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

@app.get("/players") 
async def get_players():
    try:
        cursor.execute(" SELECT * FROM CsPlayers ")
        players = cursor.fetchall()
        if not players:
            raise HTTPException(status_code=404, detail="Players not found")
        return {"players": players}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error finding players: {str(e)}") 

@app.get("/player/{player_name}")
def get_player_by_name(player_name: str):
    try:
        cursor.execute(" SELECT * FROM CsPlayers WHERE name = %s", (player_name,))
        player = cursor.fetchone()
        if not player:
            raise HTTPException(status_code=404, detail="Player Not Found")
        return {"player": player}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error finding player: {str(e)}")
 
@app.get("/stats/{player_name}")
async def get_stats(player_name: str):
    try:
        cursor.execute(""" 
                      SELECT p.name, p.team, p.kills, p.deaths, p.kd_ratio, p.headshot_pct, p.image_url 
                      FROM CsPlayers p 
                      WHERE p.name = %s 
                      
                      """, {player_name,})
        stats = cursor.fetchone()
        if not stats:
            raise HTTPException(status_code=404, detail="Player Stats Not Found")
        return {"stats", stats}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error finding player stats: {str(e)}")
        

@app.get("/matches")
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