from sqlalchemy import Column, Integer, String, Float, DateTime 
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, timezone

Base = declarative_base()


class Player(Base):
    __tablename__="CsPlayers"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    player_id = Column(String, index=True)
    team = Column(String)
    kills = Column(Integer)
    deaths = Column(Integer)
    kd_ratio = Column(Float)
    rating = Column(Float)
    headshot_pct = Column(Float)
    image_url = Column(String)
    last_updated = Column(DateTime, default=datetime.now(timezone.utc))
    
class Matches(Base):
    __tablename__="Matches"
    
    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime)
    team1_name = Column(String)
    team2_name = Column(String)
    team1_score = Column(Integer)
    team2_score = Column(Integer) 
    map_name = Column(String)
    match_result = Column(String)
    
    
    
