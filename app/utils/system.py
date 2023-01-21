import aiofiles
from aiofiles import os

from app.settings.main import settings


async def create_wg_data_dir():
    if not await os.path.exists(settings.WG_DATA_DIR_PATH):
        await os.makedirs(settings.WG_DATA_DIR_PATH)
    if not await os.path.exists(settings.USERS_FILE_PATH):
        async with aiofiles.open(settings.USERS_FILE_PATH, "w", encoding="utf-8") as file:
            await file.write("[]")
