from http.client import responses

import requests
from typing import Any

from pkg_resources import non_empty_lines

BASE = "https://pokeapi.co/api/v2"

def get_json(url: str, timeout: float =10) -> dict[str, Any]:
    response = requests.get(url, timeout=timeout)
    response.raise_for_status()
    return response.json()

def get_pokemon_core(name_or_id: str|int):
    return get_json(f"{BASE}/pokemon/{name_or_id}")
def get_species(name_or_id: str|int):
    return get_json(f"{BASE}/pokemon-species/{name_or_id}")
def get_evolution_chain(species_json: dict):
    return get_json(species_json["evolution_chain"]["url"])

def find_node(node: dict, species_name: str) -> dict | None:
    if node["species"]["name"] == species_name:
        return node

    for child in node.get("evolves_to", []):
        found = find_node(child, species_name)
        if found:
            return found

     #case none found
    return None



# need to call specific endpoint for chain info by category
data = get_pokemon_core("pikachu")
species = get_species("pikachu")
evolutionData = get_evolution_chain(species)

root = evolutionData["chain"]
evolves_to = root["evolves_to"]
print("name:", data["name"])
print("weight:", data["weight"])
print("height:", data["height"])

print("Species name: ", species["name"])

if evolves_to:
    first_child_name = evolves_to[0]["species"]["name"]
    print("Root species: ", root["species"]["name"])
    print("Evolves to (first branch): ", first_child_name)
else:
    print("This root does not evolve further")


pikachu_node = find_node(root, "pikachu")
if pikachu_node:
    next_forms = [c["species"]["name"] for c in pikachu_node["evolves_to"]]
    print("Pikachu evolves to:", next_forms or "(no further evolutions)")
