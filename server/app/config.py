import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent.parent / ".env")


def _database_url() -> str:
    url = os.environ.get("DATABASE_URL", "")
    # SQLAlchemy needs the driver name; plain postgres URLs default to psycopg 3.
    if url.startswith("postgresql://"):
        return url.replace("postgresql://", "postgresql+psycopg://", 1)
    return url


DATABASE_URL = _database_url()
JWT_SECRET = os.environ.get("JWT_SECRET", "")
TOKEN_TTL_DAYS = 7
