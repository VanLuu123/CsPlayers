from pydantic import BaseSettings 

class Settings(BaseSettings):
    DB_HOST: str 
    DB_NAME: str 
    DB_USER: str
    DB_PASS: str 
    DB_PORT: str= "5432" 
    ALLOWED_ORIGINS: list[str] = ["http://0.0.0.0:8000/"]
    
    class Config:
        env_file = ".env"
        
settings = Settings() 