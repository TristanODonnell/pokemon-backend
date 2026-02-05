# models.py
from typing import List, Optional
from pydantic import BaseModel

class SpriteUrls(BaseModel):
    """ Container for various image assets.
    'official' refers to high-resolution artwork from the 'other' API key.
    """
    default: Optional[str] = None
    official: Optional[str] = None

class EvolutionInfo(BaseModel):
    root: str
    current_index: int
    stages: List[str]

class PokemonCard(BaseModel):
    """ The final 'Clean' representation of a Pokemon.
    This model is returned directly by the API to the frontend.
    """

    id: int
    name: str
    height: int
    weight: int
    types: List[str]          # <— was list[str]
    sprites: SpriteUrls       # <— was sprite (singular)
    description: Optional[str] = None
    evolution: EvolutionInfo
