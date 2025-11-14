# models.py
from typing import List, Optional
from pydantic import BaseModel

class SpriteUrls(BaseModel):
    default: Optional[str] = None
    official: Optional[str] = None

class EvolutionInfo(BaseModel):
    root: str
    current_index: int
    stages: List[str]

class PokemonCard(BaseModel):
    id: int
    name: str
    height: int
    weight: int
    types: List[str]          # <— was list[str]
    sprites: SpriteUrls       # <— was sprite (singular)
    description: Optional[str] = None
    evolution: EvolutionInfo
