from fastapi import APIRouter 
from endpoints import players, matches 

router = APIRouter() 
router.include_router(players.router) 
router.include_router(matches.router)