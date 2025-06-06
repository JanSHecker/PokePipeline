from pydantic import BaseModel
from typing import List, Optional

class PokemonCreate(BaseModel):
    name: str

class Type(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True

class Move(BaseModel):
    id: int
    name: str
    power: Optional[int]
    accuracy: Optional[int]
    pp: Optional[int]
    type: Optional[Type]

    class Config:
        orm_mode = True

class Pokemon(PokemonCreate):
    id: int
    types: Optional[List[Type]] = []
    moves: Optional[List[Move]] = []

    class Config:
        orm_mode = True
