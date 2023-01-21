from fastapi import FastAPI

from app.api import router
from app.utils.system import create_wg_data_dir

app = FastAPI()
app.include_router(router)


@app.on_event("startup")
async def startup_event():
    await create_wg_data_dir()
