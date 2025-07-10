from sqlalchemy import Column, Integer, String, Float, DateTime 
from db.database import Base 
from datetime import datetime 

class Player(Base):
    __tablename__="CsPlayers"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    team = Column(String)
    kills = Column(Integer)
    deaths = Column(Integer)
    kd_ratio = Column(Float)
    rating = Column(Float)
    headshot_pct = Column(Float)
    image_url = Column(String)
    last_updated = Column(DateTime, default=datetime.utcnow)
