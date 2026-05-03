import psycopg2
from psycopg2 import pool
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL:
    connection_pool = psycopg2.pool.SimpleConnectionPool(1, 10, dsn=DATABASE_URL)
else:
    connection_pool = psycopg2.pool.SimpleConnectionPool(1, 10,
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT", 5432),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )