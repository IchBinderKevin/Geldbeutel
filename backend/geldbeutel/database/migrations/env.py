import asyncio
import os
import sys
from logging.config import fileConfig
from pathlib import Path
from sqlalchemy.ext.asyncio import create_async_engine

from sqlalchemy import pool

from alembic import context


def load_env_file():
    path = Path(__file__).resolve()
    for parent in path.parents:
        env_file = parent / ".env"
        if env_file.exists():
            with open(env_file) as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith("#") or "=" not in line:
                        continue
                    key, value = line.split("=", 1)
                    os.environ.setdefault(key.strip(), value.strip())
            return


# Necessary for local execution
load_env_file()


def find_project_root() -> Path:
    for parent in Path(__file__).resolve().parents:
        if (parent / "pyproject.toml").exists():
            return parent
    raise RuntimeError("Project root not found")


# Add project root to path
sys.path.append(str(find_project_root() / "geldbeutel"))

# Import project files here after the path trickey
from model.domain import BaseDomainModel
from database.db import build_database_url

database_url = build_database_url()
# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config
config.set_main_option("sqlalchemy.url", database_url)

# Interpret the config file for Python logging.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Use SQLAlchemy metadata for autogenerate
target_metadata = BaseDomainModel.metadata


# --- Async migration runner ---
async def run_migrations_online():
    connectable = create_async_engine(database_url, poolclass=pool.NullPool)

    async with connectable.connect() as conn:
        async with conn.begin():
            await conn.run_sync(do_run_migrations)

    await connectable.dispose()


def do_run_migrations(connection):
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


if context.is_offline_mode():
    raise RuntimeError("Offline mode not supported for async SQLite")

asyncio.run(run_migrations_online())
