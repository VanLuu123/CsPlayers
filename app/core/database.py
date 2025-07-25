import psycopg2
from psycopg2.extras import RealDictCursor
import time
from app.config import settings



def get_db_connection():
    while True:
        try:
            conn = psycopg2.connect(
                host=settings.DB_HOST, 
                database=settings.DB_NAME, 
                user=settings.DB_USER, 
                password=settings.DB_PASS, 
                cursor_factory=RealDictCursor)
            print("Database connection was successful")
            return conn
        except Exception as error:
            print("Connection to database failed")
            print("Error: ", error)
            time.sleep(5)