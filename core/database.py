import psycopg2
import os
from dotenv import load_dotenv
from psycopg2.extras import RealDictCursor
import time



def get_db_connection():
    load_dotenv()
    while True:
        try:
            conn = psycopg2.connect(
                host=os.getenv("DB_HOST"), 
                database=os.getenv("DB_NAME"), 
                user=os.getenv("DB_USER"), 
                password=os.getenv("DB_PASS"), 
                cursor_factory=RealDictCursor)
            cursor = conn.cursor()
            print("Database connection was successful")
            break
        except Exception as error:
            print("Connection to database failed")
            print("Error: ", error)
            time.sleep(5)