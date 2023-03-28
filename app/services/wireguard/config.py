import logging
import subprocess
from typing import List, Dict

import aiofiles

from app.models.user import User, UserStatistic
from app.services.wireguard.base import BaseWireguardService
from app.settings.wireguard import wireguard_settings

logger = logging.getLogger(__name__)


class ConfigWireguardServiceImpl(BaseWireguardService):
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

        ConfigWireguardServiceImpl.restart_wireguard_service()

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
    def get_peers_statistic() -> Dict[str, UserStatistic]:
        r = subprocess.run("wg show", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output = r.stdout.decode()

        peers_statistic = {}
        for peer_statistic in output.split("\n\n")[1:]:
            lines = peer_statistic.split("\n")
            peers_statistic[lines[0].split(": ")[1]] = UserStatistic.parse_obj({
                splitted_line[0].replace(" ", "_"): splitted_line[1]
                for line in lines[1:] if (splitted_line := line.strip().split(": ", 1))
            })
        return peers_statistic
