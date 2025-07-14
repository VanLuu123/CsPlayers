from pydantic import BaseModel 
from typing import Optional 
from datetime import datetime 

class PlayerSchema(BaseModel):
    id: int 
    name: str
    team: str
    kills: int 
    deaths: int 
    kd_ratio: int 
    rating: Optional[int]
    headshot_pct: int 
    image_url: Optional[str]
    last_updated: Optional[datetime]
    
class MatchesSchema(BaseModel):
    id: int 
    date: Optional[datetime]
    team1_name: str 
    team2_name: str 
    team1_score: int 
    team2_score: int 
    map_name: str 
    match_result: str