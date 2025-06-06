from pydantic import BaseModel

class PokemonCreate(BaseModel):
    name: str

class Pokemon(PokemonCreate):
    id: int

    class Config:
        orm_mode = True