import strawberry
from typing import List
from .types import PokemonType,TypeType,MoveType
from .. import database, models
from sqlalchemy.orm import Session

@strawberry.type
class Query:
    @strawberry.field
    def pokemons(self, info) -> List[PokemonType]:
        db = next(database.get_db())
        pokemons = db.query(models.Pokemon).all()
        return [PokemonType(id=p.id, name=p.name) for p in pokemons]
    @strawberry.field
    def pokemon(self, info, id: int) -> PokemonType:
        db = next(database.get_db())
        p = db.query(models.Pokemon).filter_by(id=id).first()
        if not p:
            raise Exception("Pokemon not found")
        return PokemonType(id=p.id, name=p.name)
    @strawberry.field
    def types(self, info) -> List[TypeType]:
        db = next(database.get_db())
        types = db.query(models.Type).all()
        return [TypeType(id=t.id, name=t.name) for t in types]

    @strawberry.field
    def moves(self, info) -> List[MoveType]:
        db = next(database.get_db())
        moves = db.query(models.Move).all()
        return [
            MoveType(
                id=m.id,
                name=m.name,
                power=m.power,
                accuracy=m.accuracy,
                pp=m.pp,
                type=TypeType(id=m.type.id, name=m.type.name) if m.type else None
            )
            for m in moves
        ]

