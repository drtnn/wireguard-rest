import subprocess
from typing import List

import aiofiles

from app.models.user import User
from app.settings.wireguard import wireguard_settings


class WireguardService:
    configuration_file_path: str = wireguard_settings.WIREGUARD_FILE_PATH

    @staticmethod
    async def update_configuration(users: List[User]):
        blocks = [
            "[Interface]\n"
            f"PrivateKey = {wireguard_settings.WIREGUARD_PRIVATE_KEY}\n"
            f"Address = {wireguard_settings.WIREGUARD_ADDRESS}\n"
            f"ListenPort = {wireguard_settings.WIREGUARD_LISTEN_PORT}\n"
            f"PostUp = {wireguard_settings.WIREGUARD_POST_UP}\n"
            f"PostDown = {wireguard_settings.WIREGUARD_POST_DOWN}\n"
        ]

        for user in users:
            blocks.append(
                "[Peer]\n"
                f"PublicKey = {user.public_key}\n"
                f"AllowedIPs = {user.address}\n"
            )

        async with aiofiles.open(wireguard_settings.WIREGUARD_FILE_PATH, "w", encoding="utf-8") as file:
            await file.write("\n".join(blocks))

        WireguardService.restart_wireguard_service()

    @staticmethod
    def restart_wireguard_service():
        return subprocess.run(
            "systemctl restart wg-quick@wg0", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )

    @staticmethod
    def generate_private_key() -> str:
        r = subprocess.run("wg genkey", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return r.stdout.decode().replace("\n", "")

    @staticmethod
    def generate_public_key(private_key: str) -> str:
        r = subprocess.run(
            f"echo \"{private_key}\" | wg pubkey", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        return r.stdout.decode().replace("\n", "")

    @staticmethod
    def generate_peer_configuration(user: User):
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
