from sqlalchemy.orm import Session
from . import models, schemas

def get_pokemon(db: Session):
    return db.query(models.Pokemon).all()

def create_pokemon(db: Session, pokemon: schemas.PokemonCreate):
    db_pokemon = models.Pokemon(name=pokemon.name)
    db.add(db_pokemon)
    db.commit()
    db.refresh(db_pokemon)
    return db_pokemon
