""" This script is for importing a JSON file with mappings from ddragon API for
    champion_id: champion_name key value pairs for faster mappings. If the file is
    created outside directory, move to backend/rift-rewind-backend/data. 
    
    In the case of Riot releasing new charactera, there is two options:
        1. Rerun the script, which will overwrite the current champions.json file with up to date mappings
        2. Change the overall structure to use ddragon API dynamically instead of using a static JSON file
"""
import json
import requests


url = "https://ddragon.leagueoflegends.com/cdn/14.21.1/data/en_US/champion.json"

response = requests.get(url)
data = response.json()


champion_map = {}
for champ_name, champ_info in data["data"].items():
    champion_id = champ_info["key"]   # numeric ID (as string)
    champion_map[champion_id] = champ_info["name"]

# Save as a smaller file
with open("champions.json", "w") as f:
    json.dump(champion_map, f, indent=4)

