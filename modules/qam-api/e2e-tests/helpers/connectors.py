"""Managers, clients and related methods to interact with the API or services."""

import requests

from .constants import IDENTITY, SERVICE_URL


class Connectors:
    """Bundle class to containing needed managers, clients or methods.

    To interact with module and validate its features.
    """

    def __init__(self) -> None:
        """Build instance."""
        self.requester = requests.Session()
        # Keep identity context if provided by caller/environment.
        if IDENTITY:
            self.requester.headers.update({"X-Identity": IDENTITY})
        self.service_url = SERVICE_URL
