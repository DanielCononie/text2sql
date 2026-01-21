import os
from sqlalchemy import create_engine, text

DATABASE_URL = os.getenv("PG_URL");

engine = create_engine(
    DATABASE_URL,
    pool_size=5,
    max_overflow=5,
    pool_pre_ping=True,  # checks dead connections
)
