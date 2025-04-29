import requests
from flask import Flask, request

app = Flask(__name__)
teams_data = {}
current_team_id = 1  

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
def create_team():
    global current_team_id
    
    request_data = request.get_json()
    
    if not request_data or 'user' not in request_data or 'team' not in request_data:
        return ({"error": "Formato inválido. Use {'user': 'nome', 'team': ['pokemon1', 'pokemon2']}"}), 400
    
    user = request_data['user']
    pokemon_names = request_data['team']
    
    team_pokemons = []
    
    for name in pokemon_names:
        pokemon = get_pokemon_data(name)
        if pokemon:
            team_pokemons.append(pokemon)
        else:
            print(f"Pokémon {name} não encontrado")
    
    while str(current_team_id) in teams_data:
        current_team_id += 1
    
    team_id = str(current_team_id)
    teams_data[team_id] = {
        "owner": user,
        "pokemons": team_pokemons
    }
    
    current_team_id += 1 
    
    return ({
        "message": "Time criado com sucesso!",
        "team_id": team_id,
        "team": teams_data[team_id]
    }), 201

@app.route('/api/teams', methods=['GET'])
def get_all_teams():
    return teams_data

@app.route('/api/teams/<user>')
def get_user_teams(user):
    user_teams = {
        team_id: team 
        for team_id, team in teams_data.items() 
        if team["owner"] == user
    }
    
    if not user_teams:
        return ({"error": f"Nenhum time encontrado para {user}"}), 404
    
    return user_teams

if __name__ == '__main__':
    app.run(debug=True)