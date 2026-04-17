import os

from sqlalchemy import event
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

DEFAULT_DB_PATH = "./data/geldbeutel.db"

def build_database_url() -> str:
    """
    Builds the database URL based on potentially existing envs
    """
    db_path = os.getenv("DB_PATH", DEFAULT_DB_PATH)
    return f"sqlite+aiosqlite:///{db_path}"

engine = create_async_engine(build_database_url(), echo=False)

AsyncSessionLocal = async_sessionmaker(
    engine,
    expire_on_commit=False
)

@event.listens_for(engine.sync_engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    """
    Event listener to set SQLite PRAGMA settings on each new connection to allow for CASCADE deletes.
    """
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()
