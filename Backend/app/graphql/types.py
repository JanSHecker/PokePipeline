import strawberry
from typing import List
from strawberry.types import Info
from app import models, database

@strawberry.type
class PokemonType:
    id: int
    name: str

    @strawberry.field
    def types(self, info: Info) -> List["TypeType"]:
        db = next(database.get_db())
        pokemon = db.query(models.Pokemon).filter(models.Pokemon.id == self.id).first()
        return [TypeType(id=t.id, name=t.name) for t in pokemon.types]

    @strawberry.field
    def moves(self, info: Info) -> List["MoveType"]:
        db = next(database.get_db())
        pokemon = db.query(models.Pokemon).filter(models.Pokemon.id == self.id).first()
        return [MoveType(id=m.id, name=m.name) for m in pokemon.moves]

@strawberry.type
class MoveType:
    id: int
    name: str

    @strawberry.field
    def type(self, info: Info) -> "TypeType":
        db = next(database.get_db())
        move = db.query(models.Move).filter(models.Move.id == self.id).first()
        return TypeType(id=move.type.id, name=move.type.name)

    @strawberry.field
    def pokemons(self, info: Info) -> List["PokemonType"]:
        db = next(database.get_db())
        move = db.query(models.Move).filter(models.Move.id == self.id).first()
        return [PokemonType(id=p.id, name=p.name) for p in move.pokemons]


@strawberry.type
class TypeType:
    id: int
    name: str
    power: int
    accuracy: int
    pp: int

    @strawberry.field
    def moves(self, info: Info) -> List["MoveType"]:
        db = next(database.get_db())
        type_obj = db.query(models.Type).filter(models.Type.id == self.id).first()
        return [MoveType(id=m.id, name=m.name) for m in type_obj.moves]

    @strawberry.field
    def pokemons(self, info: Info) -> List["PokemonType"]:
        db = next(database.get_db())
        type_obj = db.query(models.Type).filter(models.Type.id == self.id).first()
        return [PokemonType(id=p.id, name=p.name) for p in type_obj.pokemons]

