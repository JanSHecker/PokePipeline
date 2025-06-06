import strawberry
from typing import List
from strawberry.types import Info
from .. import database, models
from .types import PokemonType
import httpx
import random

@strawberry.type
class Mutation:
    @strawberry.mutation
    def delete_all_pokemon(self, info: Info) -> bool:
        db = next(database.get_db())
        db.query(models.Pokemon).delete()
        db.commit()
        return True
    @strawberry.mutation
    def add_pokemon(self, info: Info) -> bool:
        db = next(database.get_db())

        num_pokemon = 15
        total_pokemon = 1118 
        random_ids = random.sample(range(1, total_pokemon + 1), num_pokemon)


        query = f"""
        query {{
        pokemon_v2_pokemon(where: {{id: {{_in: {random_ids}}}}}) {{
            id
            name
            pokemon_v2_pokemontypes {{
            pokemon_v2_type {{ 
                id
                name
            }}
            }}
            pokemon_v2_pokemonmoves {{
            level
            pokemon_v2_move {{
                id
                name
                power
                accuracy
                pp
                pokemon_v2_type {{
                id
                name
                }}
            }}
            }}
        }}
        }}
        """

        response = httpx.post(
            "https://beta.pokeapi.co/graphql/v1beta",
            json={"query": query}
        )

        if response.status_code == 200:
            pokemons = response.json()["data"]["pokemon_v2_pokemon"]
            for p in pokemons:
            # Check if Pokémon already exists
                existing_pokemon = db.query(models.Pokemon).filter_by(id=p["id"]).first()
                if existing_pokemon:
                    continue

                # Create Pokémon
                pokemon = models.Pokemon(id=p["id"], name=p["name"])
                db.add(pokemon)

                # Add types
                for t in p["pokemon_v2_pokemontypes"]:
                    type_data = t["pokemon_v2_type"]
                    type_id = type_data["id"]
                    type_obj = db.query(models.Type).filter_by(id=type_id).first()
                    if not type_obj:
                        type_obj = models.Type(id=type_id, name=type_data.get("name"))
                        db.add(type_obj)
                        db.flush()
                    pokemon.types.append(type_obj)

                # Add moves
                for m in p["pokemon_v2_pokemonmoves"]:
                    move_data = m["pokemon_v2_move"]
                    move_id= move_data["id"]
                    move_obj = db.query(models.Move).filter_by(id=move_id).first()
                    if not move_obj:
                        move_type_id = move_data["pokemon_v2_type"]["id"] if move_data["pokemon_v2_type"] else None
                        move_type = None
                        if move_type_id:
                            move_type = db.query(models.Type).filter_by(id=move_type_id).first()
                            if not move_type:
                                move_type = models.Type(id=move_type_id, name=move_data["pokemon_v2_type"].get("name"))
                                db.add(move_type)
                                db.flush()
                        move_obj = models.Move(
                            id=move_id,
                            name=move_data.get("name"),
                            power=move_data.get("power"),
                            accuracy=move_data.get("accuracy"),
                            pp=move_data.get("pp"),
                            type=move_type
                        )
                        db.add(move_obj)
                        db.flush()

                    pokemon.moves.append(move_obj)

            db.commit()
            return True





