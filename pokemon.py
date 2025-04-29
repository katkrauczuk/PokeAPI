import requests
from flask import Flask, request

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
    pokemons_teams_id = request.get_json()

    if not pokemons_teams_id:
        return {"message": "Envie os times no formato {'time_id': ['pokemon1', 'pokemon2']}"}, 400

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
def get_user_teams(user):
    user_teams = {}
    
    for team_id, team_data in teams_data.items():
        if team_data["owner"] == user: 
            user_teams[team_id] = {
                "pokemons": team_data["pokemons"]
            }
    
    if not user_teams:
        return {"error": f"Nenhum time encontrado para o usuário {user}"}, 404
    
    return {
        "owner": user,
        "teams": user_teams
    }

if __name__ == '__main__':
    app.run(debug=True)