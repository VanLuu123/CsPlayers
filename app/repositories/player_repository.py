from typing import List, Optional 
from sqlalchemy.orm import Session 
from sqlalchemy.exc import SQLAlchemyError 
from app.core.models import Player 
from datetime import datetime, timezone
import logging 

logger = logging.getLogger(__name__) 

class PlayerRepository:
    def __init__(self, db: Session):
        self.db = db 

    def get_all(self) -> List[Player]:
        """ Get all players from database """
        try:
            return self.db.query(Player).all()
        except SQLAlchemyError as e:
            logger.error(f"Error fetching all players: {e}")
            raise 
    
    def get_by_id(self, player_id: str) -> Optional[Player]:
        """ Get a player by ID """
        try:
            return self.db.query(Player).filter(Player.player_id == player_id).first() 
        except SQLAlchemyError as e:
            logger.error(f"Error fetching player by ID: {e}")
            raise

    def get_by_name(self, name: str) -> Optional[Player]:
        """ Get a player by name """
        try:
            return self.db.query(Player).filter(Player.name == name).first() 
        except SQLAlchemyError as e:
            logger.error(f"Error fetching player by name: {e}")
            raise 

    def get_by_team(self, team: str) -> List[Player]:
        """ Get all players by team """
        try:
            return self.db.query(Player).filter(Player.team == team).all()
        except SQLAlchemyError as e:
            logger.error(f"Error fetching players by team: {e}")
            raise 

    def create(self, player_data: dict) -> Player: 
        """ Create a new player """
        try:
            player = Player(**player_data)
            self.db.add(player)
            self.db.commit()
            self.db.refresh(player) 
            logger.info(f"Created player: {player.name}")
            return player 
        except SQLAlchemyError as e:
            logger.error(f"Error creating player: {e}")
            self.db.rollback()
            raise

    def update(self, player: Player, update_data: dict) -> Player: 
        """ Update an existing player """
        try:
            for key, value in update_data.items():
                if hasattr(player, key):
                    setattr(player, key, value)
            player.last_updated = datetime.now(timezone.utc)
            self.db.commit()
            self.db.refresh(player)
            logger.info(f"Updated player: {player.name}")
            return player 
        except SQLAlchemyError as e:
            logger.error(f"Error updating player: {e}")
            self.db.rollback()
            raise 

    def upsert(self, player_data: dict) -> Player: 
        """ Create or update a player """ 
        try:
            existing_player = self.get_by_id(player_data["player_id"])
            if existing_player:
                return self.update(existing_player, player_data)
            else:
                return self.create(player_data)
        except SQLAlchemyError as e: 
            logger.error(f"Error upserting player: {e}")
            raise

    def delete(self, player: Player) -> bool:
        """ Delete a player """
        try:
            self.db.delete(player)
            self.db.commit()
            logger.info(f"Deleted player: {player.name}")
            return True
        except SQLAlchemyError as e:
            logger.error(f"Error deleting player: {e}")
            self.db.rollback()
            raise

    