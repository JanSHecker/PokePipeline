import strawberry

@strawberry.type
class PokemonType:
    id: int
    name: str
