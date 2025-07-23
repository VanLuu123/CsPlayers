# app/api/fetch_router.py

from fastapi import APIRouter, HTTPException
from data_collection.fetch_data import HLTVAPICLIENT

router = APIRouter()

@router.get("/fetch-hltv-players")
async def fetch_and_save_players():
    client = HLTVAPICLIENT()
    try:
        player_results = client.get_all_team_players()
        print(player_results[:2])  # Show first 2 players for structure
        client.save_player_stats_to_db(player_results)
        return {"status": "success", "players_fetched": len(player_results)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
