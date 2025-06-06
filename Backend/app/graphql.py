import strawberry
from typing import List
from strawberry.fastapi import GraphQLRouter
from strawberry.types import Info
import httpx

from . import models, database

@strawberry.type
class PokemonType:
    id: int
    name: str

@strawberry.type
class Query:
    @strawberry.field
    def pokemons(self) -> List[PokemonType]:
        db = next(database.get_db())
        pokemons = db.query(models.Pokemon).all()
        return [PokemonType(id=pokemon.id, name=pokemon.name) for pokemon in pokemons]

@strawberry.type
class Mutation:
    @strawberry.mutation
    def delete_all_pokemon(self, info: Info) -> bool:
        db = next(database.get_db())
        db.query(models.Pokemon).delete()
        db.commit()
        return True

    @strawberry.mutation
    def add_Pokemon(self, info: Info) -> List[PokemonType]:
        db = next(database.get_db())

        # Step 1: Get total number of Pokémon
        count_response = httpx.get("https://pokeapi.co/api/v2/pokemon?limit=1")
        total_count = count_response.json()["count"]

        # Step 2: Pick 10 unique random offsets
        import random
        offsets = random.sample(range(total_count), 10)

        # Step 3: Fetch Pokémon by offset
        new_names = []
        for offset in offsets:
            res = httpx.get(f"https://pokeapi.co/api/v2/pokemon?limit=1&offset={offset}")
            if res.status_code == 200:
                name = res.json()["results"][0]["name"]
                # Step 4: Only add if not in DB
                exists = db.query(models.Pokemon).filter(models.Pokemon.name == name).first()
                if not exists:
                    pokemon = models.Pokemon(name=name)
                    db.add(pokemon)
                    new_names.append(PokemonType(id=pokemon.id, name=name))

        db.commit()
        return new_names


schema = strawberry.Schema(query=Query, mutation=Mutation)
graphql_app = GraphQLRouter(schema)
