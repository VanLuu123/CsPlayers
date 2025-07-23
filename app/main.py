from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import uvicorn 
from app.core.database import get_db_connection
from app.core import schemas, models, database
from app.config import settings
from app.api.router import router
from app.api.fetch_router import router as fetch_router

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

@app.get("/teams")
async def get_teams():
    return {"message": "All team matches"}

@app.get("/teams/{team}")
async def get_team(team: str):
    return {"message": f"Team Match History : {team}"}


app.include_router(router)
app.include_router(fetch_router, prefix="/api")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)