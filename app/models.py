from typing import List, Optional
from pydantic import BaseModel

class SpriteUrls(BaseModel):
    #Front sprite and official artwork,
    #either one can both be none, default none
    default: Optional[str]=None
    official: Optional[str]=None

class EvolutionInfo(BaseModel):
    #stages evolution
    root: str
    current_index: int #index where current sits in stage list
    stages:  List[str]

class PokemonCard(BaseModel):
    #identy and size
    id: int
    name: str
    height: int
    weight: int

    #types listing
    types: list[str]

    #media + additional text
    sprite: SpriteUrls
    description: Optional[str] =None

    #evolution info
    evolution: EvolutionInfo