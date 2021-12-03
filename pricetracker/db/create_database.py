"""
Script to create a database. Theoretically should only be ran once locally.
"""
import psycopg2
from pricetracker.pricetracker.constants import DATABASE_NAME
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from pricetracker.pricetracker.db.config import config

config = config()

conn = psycopg2.connect(
    host="localhost", user=config["user"], password=config["password"]
)
conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

with conn.cursor() as curs:
    curs.execute(f"CREATE DATABASE {DATABASE_NAME}")

conn.close()
