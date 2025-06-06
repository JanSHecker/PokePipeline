import httpx
import random

#Makes the request to PokeAPI for new Pokemon using a set of random pokemon ids
def getPokeAPIdata():
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
        return response.json()["data"]["pokemon_v2_pokemon"]