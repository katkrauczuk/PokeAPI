import requests
from flask import Flask

app = Flask(__name__)
teams_data = {}

def get_pokemon_data(pokemon_name):
    URL_POKEAPI = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name}"
    response = requests.get(URL_POKEAPI)
    if response.status_code == 200:
        data = response.json()
        return {
            "id": data["id"],
            "name": data["name"],
            "height": data["height"],
            "weight": data["weight"]
        }

    else:  
        print(f"Erro {response.status_code} ao buscar {pokemon_name}")
        return None

@app.route('/api/teams', methods=['POST'])
def create_all_teams_pokemons():
    pokemons_teams_id = {
        "1": ["blastoise", "pikachu"],
        "2": ["blastoise", "pikachu", "venusaur", "charizard", "lapras", "psyduck"] }
    
    for team_id, pokemon_name in pokemons_teams_id.items():
        teams_pokemons = []

        for name in pokemon_name:
            pokemon = get_pokemon_data(name)
            if pokemon is not None:
                teams_pokemons.append(pokemon)
            else:  
                print(f"Não foi possível criar os time")
        
        teams_data[team_id] = {
             "owner": "katkrauczuk",
             "pokemons": teams_pokemons
        }
        print(teams_data[team_id])
    return ({"message": "Times criados com sucesso!", "teams": teams_data}), 201

@app.route('/api/teams', methods=['GET'])
def get_all_teams():
    return teams_data

@app.route('/api/teams/<user>')
def get_team1_pokemons_user(user):
    if "1" not in teams_data:
        return {"error": "Time não encontrado"}, 404
    
    team_1_data = teams_data["1"]
    
    return {
        "owner": team_1_data["owner"], 
        "pokemons": team_1_data["pokemons"]  
    }

if __name__ == '__main__':
    get_pokemon_data(pokemon_name=list)
    create_all_teams_pokemons()
    get_all_teams()
    get_team1_pokemons_user(user=str)

    app.run(debug=True)