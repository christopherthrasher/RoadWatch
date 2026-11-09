import os

import psycopg
from psycopg.rows import dict_row


def get_connection():
    return psycopg.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5433"),
        dbname=os.getenv("DB_NAME", "roadwatch"),
        user=os.getenv("DB_USER", "roadwatch"),
        password=os.getenv("DB_PASSWORD", "roadwatch_dev"),
        connect_timeout=5,
        row_factory=dict_row,
    )