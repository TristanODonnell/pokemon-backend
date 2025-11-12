from fastapi import FastAPI, HTTPException
from .models import PokemonCard
from .services.pokemon_service import PokemonService
from .services.poke_client import PokeClient

app = FastAPI(title="PokemonAPI", version="0.1.0")

_client = PokeClient()
_service = PokemonService(_client)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/pokemon/{name_or_id}", response_model=PokemonCard)
def get_pokemon(name_or_id: str):
    try:
        return _service.get_pokemon_card(name_or_id)
    except ValueError:
        # Service layer signals “not found/invalid input”
        raise HTTPException(status_code=404, detail="Pokémon not found")
    except Exception:
        # Anything else: generic server error (don’t leak details)
        raise HTTPException(status_code=500, detail="Internal error")