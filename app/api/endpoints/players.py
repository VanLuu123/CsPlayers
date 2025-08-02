from fastapi import APIRouter, Depends 
from app.core.database import get_db
from app.core.schemas import PlayerSchema 
from sqlalchemy.orm import Session
from app.core.models import CsPlayers
from app.core.exceptions import handle_database_error
from psycopg2 import DatabaseError  
from typing import List
from app.services.player_service import PlayerService
from app.repositories.player_repository import PlayerRepository
        
router = APIRouter(prefix="/players", tags=["Players"])

def get_player_service(db: Session = Depends(get_db)) -> PlayerService:
    """Dependency to get player service"""
    player_repo = PlayerRepository(db)
    return PlayerService(player_repo)

# Return List of all players
@router.get("/", response_model=List[PlayerSchema]) 
async def get_players(player_service: PlayerService = Depends(get_player_service)):
    return await player_service.get_all_players()

@router.get("/{player_name}", response_model=PlayerSchema)
async def get_player(
    player_name: str, 
    player_service: PlayerService = Depends(get_player_service)
):
    """Get a specific player by name"""
    return await player_service.get_player_by_name(player_name)

@router.get("/team/{team_name}", response_model=List[PlayerSchema])
async def get_players_by_team(
    team_name: str,
    player_service: PlayerService = Depends(get_player_service)
):
    """Get all players from a specific team"""
    return await player_service.get_players_by_team(team_name)
    
    
    