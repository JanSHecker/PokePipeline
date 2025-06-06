import strawberry
from typing import List
from strawberry.types import Info
from .. import database, models
from .types import PokemonType
import httpx
import random

@strawberry.type
class Mutation:
    @strawberry.mutation
    def delete_all_pokemon(self, info: Info) -> bool:
        db = next(database.get_db())
        db.query(models.Pokemon).delete()
        db.commit()
        return True

    @strawberry.mutation
    def add_pokemon(self, info: Info) -> bool:
        db = next(database.get_db())
        count_response = httpx.get("https://pokeapi.co/api/v2/pokemon?limit=1")
        total_count = count_response.json()["count"]
        offsets = random.sample(range(total_count), 10)

        for offset in offsets:
            res = httpx.get(f"https://pokeapi.co/api/v2/pokemon?limit=1&offset={offset}")
            if res.status_code == 200:
                name = res.json()["results"][0]["name"]
                exists = db.query(models.Pokemon).filter(models.Pokemon.name == name).first()
                if not exists:
                    pokemon = models.Pokemon(name=name)
                    db.add(pokemon)

        db.commit()
        return True
