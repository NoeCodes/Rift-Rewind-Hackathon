import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

RIOT_API_KEY = os.environ['RIOT_KEY']

def get_puuid(game_name, tag_line):
    region = "americas"  # or europe/asia depending on the player
    url = f"https://{region}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{game_name}/{tag_line}"
    headers = {"X-Riot-Token": RIOT_API_KEY}
    
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print("Error:", response.status_code, response.text)
        return None

    data = response.json()
    return data.get("puuid")
