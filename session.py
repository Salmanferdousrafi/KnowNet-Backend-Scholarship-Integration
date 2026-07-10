"""
SQLAlchemy database engine and session factory.
"""
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import get_settings

settings = get_settings()

# Convert asyncpg-style URLs to psycopg2 if needed for SQLAlchemy sync mode
DATABASE_URL = settings.database_url
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=300,
    echo=settings.debug,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Enable pgvector extension if available
@event.listens_for(engine, "connect")
def on_connect(dbapi_conn, connection_record):
    try:
        with dbapi_conn.cursor() as cursor:
            cursor.execute("CREATE EXTENSION IF NOT EXISTS vector;")
            dbapi_conn.commit()
    except Exception:
        dbapi_conn.rollback()
