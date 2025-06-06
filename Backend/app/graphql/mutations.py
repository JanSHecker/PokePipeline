import strawberry
from typing import List
from strawberry.types import Info
from .. import database, models, pokeapi, crud
from .types import PokemonType


@strawberry.type
class Mutation:
    #deletes all Pokemon from the database
    @strawberry.mutation
    def delete_all_pokemon(self, info: Info) -> bool:
        db = next(database.get_db())
        db.query(models.Pokemon).delete()
        db.commit()
        return True
    #pulls new Pokemon from the API
    @strawberry.mutation
    def add_pokemon(self, info: Info) -> bool:
        db = next(database.get_db())
        pokemons = pokeapi.getPokeAPIdata()
        crud.add_pokemons_from_api(db, pokemons)
        return True





