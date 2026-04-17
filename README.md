# Geldbeutel

A self-hosted expense-tracking / budgeting solution.

# To run in dev mode

Run a postgresql on the host (or via docker with port mapping)

Run `pnpm run dev` in frontend/ and `uv run python geldbeutel/main.py` in backend/
Vite vill proxy the api request to :3000 (if you change the backend port you need to update frontend/vite.config.ts accordingly)

# To run in "prod" mode locally

Run `docker compose up -d` in geldbeutel/

# To create a new migration

Run `alembic revision --autogenerate -m "<MIGRATION_NAME>" --rev-id <XYZ>` if you changed the sqlalchemy models.

If you want to create a migration without autogenerate use:
`alembic revision -m "<MIGRATION_NAME>" --rev-id <XYZY`

Replace MIGRATION_NAME and XYZ - the revision id like 001 - accordingly

# Techstack / Libraries / Tools

## Backend

- Python
- uv
- SQLAlchemy
- Alembic
- FastAPI

## Frontend

- React
- TypeScript
- Vite
- pnpm
- TailwindCSS
- Shadcn BaseUI Components
- Lucide Icons
