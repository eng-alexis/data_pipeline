import psycopg2
import os

from dotenv import load_dotenv
load_dotenv()

def get_db_connection ():

    conn = psycopg2.connect(
        host="localhost",
        port= os.getenv("POSTGRES_PORT"),
        database= os.getenv("POSTGRES_DB"),
        user= os.getenv("POSTGRES_USER"),
        password= os.getenv("POSTGRES_PASSWORD")
    )
 
    return conn