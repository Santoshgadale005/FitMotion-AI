"""SQLAlchemy database engine, session management, and health checks."""

from __future__ import annotations

from contextlib import contextmanager
from typing import Any, Generator

from sqlalchemy import Engine, create_engine, event, inspect, text
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

import config


class Base(DeclarativeBase):
    """Base declarative class for all FitMotion AI ORM models."""


def _enable_sqlite_foreign_keys(dbapi_connection: Any, _connection_record: Any) -> None:
    """Enforce foreign-key constraints on every SQLite connection."""
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


def create_db_engine(database_url: str | None = None) -> Engine:
    """Create a configured SQLAlchemy engine.

    Args:
        database_url: Optional override URL (useful for isolated unit tests).

    Returns:
        Configured SQLAlchemy Engine instance.
    """
    url = database_url or config.DATABASE_URL
    connect_args: dict[str, Any] = {}

    if url.startswith("sqlite"):
        # Required because Streamlit executes callbacks across threads.
        connect_args["check_same_thread"] = False

    db_engine = create_engine(
        url,
        connect_args=connect_args,
        future=True,
        pool_pre_ping=True,
    )

    if url.startswith("sqlite"):
        event.listen(db_engine, "connect", _enable_sqlite_foreign_keys)

    return db_engine


engine: Engine = create_db_engine()
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
    class_=Session,
)


def init_db(target_engine: Engine | None = None) -> None:
    """Create all database tables if they do not yet exist."""
    # Import models here so SQLAlchemy registers every table on Base.metadata.
    from database import models  # noqa: F401

    active_engine = target_engine or engine
    Base.metadata.create_all(bind=active_engine)


@contextmanager
def get_db_session(
    session_factory: sessionmaker[Session] | None = None,
) -> Generator[Session, None, None]:
    """Provide a transactional database session scope."""
    factory = session_factory or SessionLocal
    session = factory()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def check_database_health(target_engine: Engine | None = None) -> dict[str, Any]:
    """Verify database connectivity and inspect initialized tables."""
    active_engine = target_engine or engine
    try:
        with active_engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        inspector = inspect(active_engine)
        tables = sorted(inspector.get_table_names())
        return {
            "status": "connected",
            "dialect": active_engine.dialect.name,
            "database_url": str(active_engine.url),
            "tables": tables,
            "table_count": len(tables),
        }
    except Exception as exc:
        return {
            "status": "error",
            "dialect": active_engine.dialect.name,
            "database_url": str(active_engine.url),
            "tables": [],
            "table_count": 0,
            "error": str(exc),
        }


def get_table_counts(target_engine: Engine | None = None) -> dict[str, int]:
    """Return exact row counts for every initialized table in the database."""
    active_engine = target_engine or engine
    inspector = inspect(active_engine)
    counts: dict[str, int] = {}
    with active_engine.connect() as conn:
        for table_name in sorted(inspector.get_table_names()):
            result = conn.execute(text(f'SELECT COUNT(*) FROM "{table_name}"'))
            counts[table_name] = int(result.scalar_one())
    return counts
