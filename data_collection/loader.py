import logging
from typing import List, Dict, Any
from app.core.database import SessionLocal 
from sqlalchemy.orm import Session 
from app.repositories.player_repository import PlayerRepository
from app.core.exceptions import handle_database_error
from psycopg2 import DatabaseError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Loader:
    def __init__(self):
        pass

    def get_db_session(self) -> Session:
        """ Get a database session """
        return SessionLocal()
    
    def grab_players(self) -> List[Dict[str, Any]]:
        db = self.get_db_session()
        try:
            player_repo = PlayerRepository(db)
            players = player_repo.get_all()
            return [{"id": player.player_id, "name": player.name} for player in players]
        except DatabaseError as e:
            handle_database_error(DatabaseError, "fetching all players")
            raise
        finally:
            db.close()

    def upsert_players(self, players: List[Dict[str, Any]]):
        if not players:
            logger.info("No players to upsert")
            return 
        
        db = self.get_db_session()
        try:
            player_repo = PlayerRepository(db)
            
            for player in players:
                if not player.get("id") or not player.get("name"):
                    logger.warning(f"Skipping invalid player: {player}")
                    continue 
                
                upsert_query = {
                    "player_id": str(player["id"]),
                    "name": player["name"],
                }
                player_repo.upsert(upsert_query)
            logger.info(f"Successfully processed {len(players)} players.")
        except DatabaseError as e:
            handle_database_error("upserting players")
            raise 
        finally:
            db.close()
    
    def upsert_players_stats(self, player_id: int, stats):
        if not player_id or stats:
            logger.info("No player stats to upsert.")
            return None 
        
        db = self.get_db_session()
        try:
            player_repo = PlayerRepository(db)
            player = player_repo.get_by_hltv_id(str(player_id))
            if not player:
                logger.warning(f"Player with HLTV ID {player_id} not found")
                return
            
            player_repo.update(player, stats)
            logger.info(f"Successfully updated stats for player: {player.name}")
            
        except Exception as e:
            logger.error(f"Error upserting player stats: {e}")
            raise
        finally:
            db.close()


