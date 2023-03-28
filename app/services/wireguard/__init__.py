from typing import Type

from app.services.wireguard.base import BaseWireguardService
from app.services.wireguard.config import ConfigWireguardServiceImpl

WireguardService: Type[BaseWireguardService] = ConfigWireguardServiceImpl
