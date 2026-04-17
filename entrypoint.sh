#!/bin/sh
set -e

# Migrate database
uv run alembic upgrade head

# Start app
uv run python geldbeutel/main.py