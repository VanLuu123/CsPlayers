from typing import List, Optional
from fastapi import HTTPException
from app.repositories.player_repository import PlayerRepository
from app.core.schemas import PlayerSchema
from datetime import datetime, timezone
import logging 

logger = logging.getLogger(__name__)

class PlayerService:
    def __init__(self, player_repository: PlayerRepository):
        self.player_repository = player_repository
        
    async def get_all_players(self) -> List[PlayerSchema]:
        """ Grab all players from repo """
        try:
            players = self.player_repository.get_all()
            if not players:
                raise HTTPException(status_code=404, detail="No Players Found.")
            return [PlayerSchema.model_validate(player) for player in players]
        except Exception as e:
            logger.error(f"Service error: {e}")
            raise HTTPException(status_code=500, detail="Internal server error.")
        
    async def get_player_by_name(self, name: str) -> PlayerSchema:
        """ Grab player by name from repo """
        if not name or not name.strip():
            raise HTTPException(status_code=400, detail="Player name can not be empty.")
        try:
            player = self.player_repository.get_by_name(name.strip())
            if not player:
                raise HTTPException(status_code=404, detail=f"Player {name} can not be found.")
            return PlayerSchema.model_validate(player)
        except Exception as e:
            logger.error(f"Service error: {e}")
            raise HTTPException(status_code=500, detail="Internal server error.")
        
    async def get_player_by_id(self, id: int) -> PlayerSchema:
        """ Grab player by id from repo """
        if not id:
            raise HTTPException(status_code=400, detail="Player id can not be empty.")
        try:
            player = self.player_repository.get_by_id(id)
            if not player:
                raise HTTPException(status_code=404, detail=f"Player {id} can not be found.")
            return PlayerSchema.model_validate(player)
        except Exception as e:
            logger.error(f"Service error: {e}")
            raise HTTPException(status_code=500, detail="Internal server error.")
    
    async def get_players_by_team(self, team: str) -> List[PlayerSchema]:
        """ Grab players by team from repo """
        if not team or not team.strip():
            raise HTTPException(status_code=400, detail="Team can not be empty.")
        try:
            players = self.player_repository.get_by_team(team.strip())
            if not players:
                raise HTTPException(status_code=404, detail=f"Players for {team} can not be found.")
            return [PlayerSchema.model_validate(player) for player in players]
        except Exception as e:
            logger.error(f"Service error: {e}")
            raise HTTPException(status_code=500, detail="Internal server error.")
    
    async def create_update_players(self, player_data: dict) -> PlayerSchema:
        """ Create or update a player from repo """
        try:
            player_data['last_updated'] = datetime.now(timezone.utc)
            player = self.player_repository.upsert(player_data)
            return PlayerSchema.model_validate(player)
        except Exception as e:
            logger.error(f"Service error: {e}")
            raise HTTPException(status_code=500, detail="Internal server error.")
        
    
            
            
        