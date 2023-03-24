from logging.config import dictConfig

from fastapi import FastAPI

from app.api import router
from app.settings.logger import logger_config
from app.utils.system import create_wg_data_dir

app = FastAPI()
app.include_router(router)

dictConfig(logger_config.dict())


@app.on_event("startup")
async def startup_event():
    await create_wg_data_dir()
