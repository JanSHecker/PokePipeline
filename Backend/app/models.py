from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class Pokemon(Base):
    __tablename__ = "pokemon"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    types = relationship(
        "Type", 
        secondary="pokemon_type_association", 
        back_populates="pokemon",
        cascade="all, delete",
        passive_deletes=True,
    )
    moves = relationship(
        "Move", 
        secondary="pokemon_move_association", 
        back_populates="pokemon",
        cascade="all, delete",
        passive_deletes=True,
    )

class Type(Base):
    __tablename__ = "type"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    
    pokemon = relationship(
        "Pokemon",
        secondary="pokemon_type_association",
        back_populates="types",
    )

class Move(Base):
    __tablename__ = "move"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    power = Column(Integer, nullable=True)
    accuracy = Column(Integer, nullable=True)
    pp = Column(Integer, nullable=True)
    type_id = Column(Integer, ForeignKey("type.id"))
    type = relationship("Type")

 
    pokemon = relationship(
        "Pokemon",
        secondary="pokemon_move_association",
        back_populates="moves",
    )

# Association Tables 
pokemon_type_association = Table(
    "pokemon_type_association", Base.metadata,
    Column("pokemon_id", Integer, ForeignKey("pokemon.id", ondelete="CASCADE")),
    Column("type_id", Integer, ForeignKey("type.id", ondelete="CASCADE")),
)

pokemon_move_association = Table(
    "pokemon_move_association", Base.metadata,
    Column("pokemon_id", Integer, ForeignKey("pokemon.id", ondelete="CASCADE")),
    Column("move_id", Integer, ForeignKey("move.id", ondelete="CASCADE")),
)
