import requests


def get_pokemon_data(pokemon_name):
    URL_POKEAPI = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name}"
    response = requests.get(URL_POKEAPI)
    if response.status_code == 200:
        return response.json()
    else:  
        print(f"Erro {response.status_code} ao buscar {pokemon_name}")
        return None

# creates a Pokémon team with 6 specific Pokémon, searches for a team registered by user.
def get_team_pokemons():
    pokemons = ["blastoise", "pikachu", "charizard", "venusaur", "lapras", "dragonite"]
    team_data = []
    
    for name in pokemons:
        pokemon = get_pokemon_data(name)
        if pokemon is not None:
            team_data.append({
                    "owner": "katkrauczuk",
                    "pokemons": {
                    "name": pokemon["name"],
                    "id": pokemon["id"],
                    "height": pokemon["height"],
                    "weight": pokemon["weight"]
                    }
                }) 
        else:  
            print(f"Não foi possível adicionar os dados do {name} ao time")
    return team_data

all_team = get_team_pokemons()
print(all_team)