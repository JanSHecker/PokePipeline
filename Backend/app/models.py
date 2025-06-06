from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

# Association tables
pokemon_type_association = Table(
    "pokemon_type_association",
    Base.metadata,
    Column("pokemon_id", Integer, ForeignKey("pokemon.id")),
    Column("type_id", Integer, ForeignKey("types.id")),
)

pokemon_move_association = Table(
    "pokemon_move_association",
    Base.metadata,
    Column("pokemon_id", Integer, ForeignKey("pokemon.id")),
    Column("move_id", Integer, ForeignKey("moves.id")),
)

class Pokemon(Base):
    __tablename__ = "pokemon"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

    types = relationship("Type", secondary=pokemon_type_association, back_populates="pokemons")
    moves = relationship("Move", secondary=pokemon_move_association, back_populates="pokemons")

class Move(Base):
    __tablename__ = "moves"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

    type_id = Column(Integer, ForeignKey("types.id"), nullable=False)
    type = relationship("Type", back_populates="moves")

    pokemons = relationship("Pokemon", secondary=pokemon_move_association, back_populates="moves")


class Type(Base):
    __tablename__ = "types"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

    moves = relationship("Move", back_populates="type")
    pokemons = relationship("Pokemon", secondary=pokemon_type_association, back_populates="types")


