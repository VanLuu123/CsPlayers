from fastapi import HTTPException
import logging 

logger = logging.getLogger(__name__)

class DatabaseError(Exception):
    pass 

class PlayerNotFoundError(Exception):
    pass 

def handle_database_error(e: Exception, operation:str):
    logger.error(f"Database error during {operation}: {e}")
    raise HTTPException(status_code=500, detail=f"Database error during {operation}")