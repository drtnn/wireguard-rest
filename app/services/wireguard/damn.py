import logging
from typing import List

from app.models.user import User
from app.services.wireguard.base import BaseWireguardService

logger = logging.getLogger(__name__)


class DamnWireguardServiceImpl(BaseWireguardService):
    @staticmethod
    async def update_configuration(users: List[User]):
        logger.info("Wireguard configuration is updated")

    @staticmethod
    def restart_wireguard_service():
        logger.info("Wireguard service is restarted")

    @staticmethod
    def generate_private_key() -> str:
        return "SHoTR/dM97q5CXrBeUPoCoSDSOYXHAJMeBaBrcIzK2U="

    @staticmethod
    def generate_public_key(private_key: str) -> str:
        return "BRc6g8NwVRput4d0ojbNIKUuGibomTxLDXH/ZWjyWiU="
