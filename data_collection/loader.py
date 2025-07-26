import asyncio 
import logging
import os 
from typing import List, Dict, Any, Optional 
from app.core.database import get_db_connection

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Loader:
    def __init__(self):
        pass

    def upsert_players(self, players: List[Dict[str, Any]]):
        if not players:
            logger.info("No players to upsert")
            return None 
        
        upsert_query = """
            INSERT INTO "CsPlayers"(id, name, last_updated)
            VALUES (%s, %s, CURRENT_TIMESTAMP)
            ON CONFLICT (id) 
            DO UPDATE SET
                name = EXCLUDED.name,
                last_updated = EXCLUDED.last_updated
        """
        conn = None
        cursor = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            for player in players:
                if not player.get("id") or not player.get("name"):
                    logger.warning(f"Skipping invalid player data: {player}")
                    continue 
                cursor.execute(upsert_query, (player["id"], player["name"]))
            conn.commit()
            logger.info(f"Successfully processed players")
        except Exception as e:
            logger.error(f"Error upserting players: {e}")
            if conn:
                conn.rollback()
            raise
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()



