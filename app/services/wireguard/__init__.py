from typing import Type

from app.services.wireguard.base import BaseWireguardService
from app.services.wireguard.config import ConfigWireguardServiceImpl
from app.services.wireguard.damn import DamnWireguardServiceImpl
from app.settings.main import settings

WireguardService: Type[BaseWireguardService] = ConfigWireguardServiceImpl
if settings.ENVIRONMENT == "DEVELOPMENT":
    WireguardService = DamnWireguardServiceImpl
