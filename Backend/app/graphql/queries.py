import strawberry
from typing import List
from .types import PokemonType
from .. import database, models

@strawberry.type
class Query:
    @strawberry.field
    def pokemons(self) -> List[PokemonType]:
        db = next(database.get_db())
        pokemons = db.query(models.Pokemon).all()
        return [PokemonType(id=pokemon.id, name=pokemon.name) for pokemon in pokemons]
