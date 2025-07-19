from pydantic import BaseModel, Field
from typing import Optional 
from datetime import datetime 

class PlayerSchema(BaseModel):
    id: Optional[int] = None
    player_id: int
    name: str
    team: Optional[str] = None
    kills: Optional[int] = 0
    deaths: Optional[int] = 0
    kd_ratio: Optional[float] = 0.0
    rating: Optional[float] = 0.0
    headshot_pct: Optional[float] = 0.0
    kills_round: Optional[float] = 0.0  
    image_url: Optional[str] = None
    last_updated: Optional[datetime] = None

    class Config:
        from_attributes = True  # For SQLAlchemy compatibility

class MatchesSchema(BaseModel):
    id: Optional[int] = None
    date: Optional[datetime] = None
    team1_id: Optional[int] = None
    team1_name: str
    team2_id: Optional[int] = None
    team2_name: str
    team1_score: int = 0
    team2_score: int = 0
    map_name: Optional[str] = None
    match_result: Optional[str] = None
    tournament: Optional[str] = None
    match_status: Optional[str] = "completed"

    class Config:
        from_attributes = True

class PlayersResponse(BaseModel):
    players: list[PlayerSchema]

class MatchesResponse(BaseModel):
    matches: list[MatchesSchema]