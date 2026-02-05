from __future__ import annotations
from typing import Any, Optional, Union
import requests

class PokeClient:
    """ Handles low-level HTTP communication with the PokéAPI.
    Responsibilities:
    - Session management (connection pooling)
    - URL construction and normalization
    - Raising exceptions for non-200 responses
    """
    def __init__(
        self,
        base_url: str="https://pokeapi.co/api/v2",
        timeout: float=10.0,
        session: Optional[requests.Session] = None,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = session or requests.Session()

        self.session.headers.update(
            {"User-Agent": "PokemonAPIProject/0.1 (+https://pokeapi.co/)"}
        )


    #LOW LEVEL SECTION
    def _get(self, path_or_url:str) -> dict[str, Any]:
        """ Executes the HTTP GET request.
        Supports both relative paths ('pokemon/1')
        and absolute URLs (fetched from evolution chain links).
        """

        url = (
            path_or_url
            if path_or_url.startswith("http")
            else f"{self.base_url}/{path_or_url.lstrip('/')}"
        )
        resp = self.session.get(url, timeout=self.timeout)
        resp.raise_for_status()
        return resp.json()



    def get_pokemon(self, name_or_id: Union[str, int]) -> dict[str, Any]:
        """/pokemon/{name_or_id}"""
        return self._get(f"pokemon/{name_or_id}")

    def get_species(self, name_or_id: Union[str, int]) -> dict[str, Any]:
        """/pokemon-species/{name_or_id}"""
        return self._get(f"pokemon-species/{name_or_id}")

    def get_evolution_chain_by_id(self, chain_id: Union[str, int]) -> dict[str, Any]:
        """/evolution-chain/{id}"""
        return self._get(f"evolution-chain/{chain_id}")

    def get_evolution_chain_for_species(
            self, name_or_id: Union[str, int]
        ) -> dict[str, Any]:
        """ A convenience wrapper that performs a 'Follow-the-Link' operation.
        Because the evolution chain ID isn't the same as the Pokemon ID,
         we must first fetch the species to find the correct evolution URL.
         """
        species = self.get_species(name_or_id)
        evo_url = species["evolution_chain"]["url"]  # full URL from API
        return self._get(evo_url)




