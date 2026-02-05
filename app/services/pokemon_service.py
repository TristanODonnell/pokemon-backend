from __future__ import annotations
from typing import Iterable, List, Dict, Any

from .poke_client import PokeClient
from ..models import PokemonCard, SpriteUrls, EvolutionInfo

class PokemonService:
    """ Orchestrates the stitching of multiple PokeAPI endpoints.
    This layer is responsible for the 'Business Logic',
    converting the raw, fragmented data of the PokeAPI
    into a cohesive PokemonCard model for our frontend.
    """

    def __init__(self, client: PokeClient | None = None) -> None:
        # Dependency Injection: Allows us to swap in a MockClient for testing.
        self.client = client or PokeClient()

    #PUBLIC API ----
    def get_pokemon_card(self, name_or_id: str | int) -> PokemonCard:
        """ Coordinates three separate API calls to build a full data profile.
        We fetch /pokemon and /species in parallel (conceptually)
        to get the most complete view of the entity.
        """
        p = self.client.get_pokemon(name_or_id)
        species = self.client.get_species(name_or_id)

        #Basic attribute extraction
        pid= p["id"]
        pname= p["name"]
        height= p["height"]
        weight= p["weight"]

        # Types and Sprites extraction logic...
        # Note: We drill into 'official-artwork' specifically because the
        # default sprites are often too small for modern UI.
        types = [t["type"]["name"] for t in p.get("types", [])]

        sprites = p.get("sprites", {})
        official = (
            sprites.get("other", {})
            .get("official-artwork", {})
            .get("front_default")
        )
        sprite_urls = SpriteUrls(
            default=sprites.get("front_default"),
            official=official,
        )
        description = _pick_english_flavor_text(
            species.get("flavor_text_entries", [])
        )

        # Evolution Handling: Graceful Degradation
        try:
            # We wrap this in a try-block because evolution data is
            # secondary to basic stats. If the chain fails, we still
            # want to return the main Pokemon data.
            evo_chain = self.client.get_evolution_chain_for_species(name_or_id)
        except Exception:
            # Fallback to a 'null' chain if the network fails or data is missing
            evo_chain = None

        evolution = (
            self._build_evolution_info(evo_chain, pname)
            if evo_chain
            else EvolutionInfo(root=pname, current_index=0, stages=[pname])
        )
        return PokemonCard(
            id=pid,
            name=pname,
            height=height,
            weight=weight,
            types=types,
            sprites=sprite_urls,
            description=description,
            evolution=evolution,
        )

    def _build_evolution_info(self, chain: Dict[str, Any], current_species: str) -> EvolutionInfo:
        """
        Turn an evolution-chain tree into:
        - stages: ordered list of species names along the path that contains current_species
        - root: the root species of that path
        - current_index: index of current_species within stages
        Notes:
        PokeAPI chains are trees; we pick the path that includes current_species.
        """

        root_node = chain["chain"]  # tree root
        path = _find_path_to_species(root_node, current_species)
        if not path:
            # Fallback: use the root only if species not found in chain (edge-case)
            only = root_node["species"]["name"]
            return EvolutionInfo(root=only, current_index=0, stages=[only])

        stages = [node["species"]["name"] for node in path]
        current_index = stages.index(current_species)
        root = stages[0]
        return EvolutionInfo(root=root, current_index=current_index, stages=stages)

    ####HELPER FUNCTIONS
def _pick_english_flavor_text(entries: Iterable[Dict[str, Any]]) -> str | None:
    """ Filters for English text and cleans legacy console formatting.
    PokeAPI text contains '\f' (form feed) and '\n' from original GameBoy/DS internal data.
    We strip these to avoid UI rendering bugs.
    """

    # First pass: English entries
    english = [e for e in entries if e.get("language", {}).get("name") == "en"]
    if not english:
        return None

    # Heuristic: last English entry is often the most “modern” wording
    text = english[-1].get("flavor_text", "") or ""
    return text.replace("\n", " ").replace("\f", " ").strip() or None

def _find_path_to_species(node: Dict[str, Any], species_name: str) -> List[Dict[str, Any]] | None:
    """
    Depth-first search that returns the path (list of nodes) from root to the node
    whose species.name == species_name. If not found, returns None.
    Each node has:
        node["species"]["name"]
        node["evolves_to"] -> list[child_node]
    """
    if node["species"]["name"] == species_name:
        return [node]

    for child in node.get("evolves_to", []):
        path = _find_path_to_species(child, species_name)
        if path:
            return [node] + path

    return None
