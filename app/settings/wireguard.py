from pydantic import BaseSettings


class WireguardSettings(BaseSettings):
    WIREGUARD_FILE_PATH: str = "/etc/wireguard/wg0.conf"

    WIREGUARD_PUBLIC_KEY: str = "public_key"
    WIREGUARD_PRIVATE_KEY: str = "private_key"

    WIREGUARD_ADDRESS: str = "10.0.0.1/24"

    WIREGUARD_LISTEN_IP: str = "1.1.1.1"
    WIREGUARD_LISTEN_PORT: int = 51830

    WIREGUARD_POST_UP: str = "iptables -A FORWARD -i %i -j ACCEPT; iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE"
    WIREGUARD_POST_DOWN: str = "iptables -D FORWARD -i %i -j ACCEPT; iptables -t nat -D POSTROUTING -o eth0 -j MASQUERADE"

    WIREGUARD_ALLOWED_IPS: str = "0.0.0.0/0"
    WIREGUARD_PERSISTENT_KEEPALIVE: int = 20

    WIREGUARD_PEER_DNS: str = "8.8.8.8"

    @property
    def WIREGUARD_ENDPOINT(self) -> str:
        return f"{self.WIREGUARD_LISTEN_IP}:{self.WIREGUARD_LISTEN_PORT}"

    class Config:
        case_sensitive = True


wireguard_settings = WireguardSettings()
