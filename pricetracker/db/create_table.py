"""
Script to create a table. Theoretically should only be ran once locally.
"""
import psycopg2
from pricetracker.pricetracker.constants import TABLE_NAME
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from pricetracker.pricetracker.db.config import config

config = config()

conn = psycopg2.connect(
    host="localhost",
    database=config["database"],
    user=config["user"],
    password=config["password"],
)
conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

with conn.cursor() as curs:
    curs.execute(
        f"CREATE TABLE {TABLE_NAME} (product_name text, price integer, scrape_date date default CURRENT_DATE"
    )

conn.close()
