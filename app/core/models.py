from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship 
from datetime import datetime, timezone

Base = declarative_base()


class Player(Base):
    __tablename__="CsPlayers"
    
    id = Column(Integer, primary_key=True, index=True)
    player_id = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, index=True, nullable=False)
    team = Column(String, nullable=True)
    kills = Column(Integer, default=0)
    deaths = Column(Integer, default=0)
    kd_ratio = Column(Float, default=0)
    rating = Column(Float, default=0)
    headshot_pct = Column(Float, default=0)
    image_url = Column(Text, nullable=True)
    last_updated = Column(DateTime, default=datetime.now(timezone.utc))

    def __repr__(self):
        return f"<Player(name='{self.name}', team='{self.team}')>" 
    
class Matches(Base):
    __tablename__="Matches"
    
    id = Column(Integer, primary_key=True, index=True)
    match_id = Column(String, unique=True, index=True, nullable=False) 
    date = Column(DateTime, nullable=False)
    team1_name = Column(String, nullable=False)
    team2_name = Column(String, nullable=False)
    team1_score = Column(Integer, default=0)
    team2_score = Column(Integer, default=0)
    map_name = Column(String, nullable=True)
    match_result = Column(String, nullable=True)  
    tournament = Column(String, nullable=True)
    match_status = Column(String, default="completed")
    
    def __repr__(self):
        return f"<Match({self.team1_name} vs {self.team2_name})>"
    
    
    
