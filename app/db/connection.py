import psycopg2
from psycopg2 import pool
from dotenv import load_dotenv
import os
load_dotenv()

connection_pool = psycopg2.pool.SimpleConnectionPool(1, 10,
    host=os.getenv("DB_HOST"), 
    database=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD")
)


def get_db_connection():
    conn = connection_pool.getconn()
    try:
        yield conn
    finally:
        connection_pool.putconn(conn)