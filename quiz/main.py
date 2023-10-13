from contextlib import asynccontextmanager

from fastapi import FastAPI

from config import settings
from db_layer.db_engine import sessionmanager
from entrypoints.main_router import main_router


def init_app(init_db=True):
    lifespan = None

    if init_db:
        sessionmanager.init(settings.database_url)

        @asynccontextmanager
        async def lifespan(app: FastAPI):
            yield
            if sessionmanager._engine is not None:
                await sessionmanager.close()

    app = FastAPI(title=settings.app_title, lifespan=lifespan)
    app.include_router(main_router)
    return app


app = init_app()
