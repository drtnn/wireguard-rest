import os

from pydantic import BaseSettings


class Settings(BaseSettings):
    WG_DATA_DIR_PATH: str = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))), "wg-data"
    )
    USERS_FILE_PATH: str = os.path.join(WG_DATA_DIR_PATH, "users.json")

    class Config:
        case_sensitive = True


settings = Settings()
