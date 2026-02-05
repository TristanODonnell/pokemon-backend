from fastapi import APIRouter, FastAPI, HTTPException
from .models import PokemonCard
from .services.pokemon_service import PokemonService
from .services.poke_client import PokeClient

router = APIRouter(tags=["pokemon"])

# Dependencies initialized at module level for shared state
_client = PokeClient()
_service = PokemonService(_client)


@router.get("/health") # get health request function
def health():
    return {"status": "ok"}

@router.get("/pokemon/{name_or_id}", response_model=PokemonCard) # Pokemon request function
def get_pokemon(name_or_id: str):
    """ Fetch a Pokémon card by name or numerical ID.
    Errors:
    - 404: Invalid name or ID
    - 500: Connection or processing failure
    """
    try:
        # We delegate to the service layer to keep the API route "thin"
        # and focused only on HTTP concerns.
        return _service.get_pokemon_card(name_or_id)
    except ValueError:
        # ValueError is our internal signal that the resource doesn't exist.
        # We map this to a 404 so the frontend knows to show a "Not Found" state.
        raise HTTPException(status_code=404, detail="Pokémon not found")
    except Exception:
        # Catch-all protects the server from leaking sensitive tracebacks
        # while ensuring the client receives a valid JSON error.
        raise HTTPException(status_code=500, detail="Internal error")