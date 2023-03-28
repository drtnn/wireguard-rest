from abc import ABC, abstractmethod
from typing import List, Dict

from app.models.user import User, UserStatistic
from app.settings.wireguard import wireguard_settings


class BaseWireguardService(ABC):
    @staticmethod
    @abstractmethod
    async def update_configuration(users: List[User]):
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def restart_wireguard_service():
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def generate_private_key() -> str:
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def generate_public_key(private_key: str) -> str:
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def get_peers_statistic() -> Dict[str, UserStatistic]:
        raise NotImplementedError

    @staticmethod
    def generate_peer_configuration(user: User) -> str:
        return (
            "[Interface]\n"
            f"PrivateKey = {user.private_key}\n"
            f"Address = {user.address}\n"
            f"DNS = {wireguard_settings.WIREGUARD_PEER_DNS}\n\n"

            "[Peer]\n"
            f"PublicKey = {wireguard_settings.WIREGUARD_PUBLIC_KEY}\n"
            f"Endpoint = {wireguard_settings.WIREGUARD_ENDPOINT}\n"
            f"AllowedIPs = {wireguard_settings.WIREGUARD_ALLOWED_IPS}\n"
            f"PersistentKeepalive = {wireguard_settings.WIREGUARD_PERSISTENT_KEEPALIVE}\n"
        )
