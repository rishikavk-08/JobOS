import os

import psycopg
from dotenv import load_dotenv

load_dotenv()


def get_connection():
    return psycopg.connect(
        host=os.getenv("POSTGRES_HOST", "localhost"),
        port=os.getenv("POSTGRES_PORT", "5432"),
        dbname=os.getenv("POSTGRES_DB", "jobos"),
        user=os.getenv("POSTGRES_USER", "jobos"),
        password=os.getenv("POSTGRES_PASSWORD", "dbpass"),
    )
