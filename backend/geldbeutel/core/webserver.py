import os

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from uvicorn.config import Config
from uvicorn.server import Server

from api.account_router import create_account_router

FRONTEND_DIST = "./dist"


class Webserver:
    """
    Webserver for serving the FastAPI and the frontend in production.
    Has as deployment mode to only serve the frontend in production as it is directly served by vite in development.
    """

    def __init__(self):
        self.app = FastAPI()

        self.app.include_router(create_account_router(), prefix="/api/accounts")

        if os.getenv("DEPLOYMENT_MODE") == "docker":
            self.app.mount(
                "/assets",
                StaticFiles(directory=os.path.join(FRONTEND_DIST, "assets")),
                name="assets",
            )

            async def serve_spa(full_path: str):
                file = os.path.join(FRONTEND_DIST, full_path)
                if os.path.isfile(file):
                    return FileResponse(file)
                return FileResponse(os.path.join(FRONTEND_DIST, "index.html"))

            self.app.add_api_route("/{full_path:path}", serve_spa, methods=["GET"])

    async def run_server(self):
        """
        Starts the api server.
        """
        config = Config(self.app, host="0.0.0.0", port=3000, log_config=None)
        server = Server(config)
        await server.serve()
