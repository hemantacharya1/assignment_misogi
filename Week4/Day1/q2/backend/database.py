from __future__ import annotations

import os
from typing import Iterator

from sqlmodel import SQLModel, Session, create_engine
from dotenv import load_dotenv

# Load environment variables from .env file located at project root or backend dir
load_dotenv()

DATABASE_URL: str = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg://postgres:password@localhost:5432/dummy",
)

# echo can be toggled via env
engine = create_engine(DATABASE_URL, echo=os.getenv("SQL_ECHO", "false").lower() == "true")


def init_db() -> None:
    """Create all tables (no-op if they already exist)."""
    SQLModel.metadata.create_all(engine)


def get_session() -> Iterator[Session]:
    """Yield a new SQLModel session (FastAPI dependency)."""
    with Session(engine) as session:
        yield session 