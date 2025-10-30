import os
import requests
from dotenv import load_dotenv
from datetime import datetime

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

def get_match_ids_last_year(puuid):
    start_time = 1735689600 # Unix time stamp for the start of 2025
    end_time = int(datetime.now().timestamp())
    start = 0
    all_ids = []

    while True:
        url = f"https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids"
        params = {
            "startTime": start_time,
            "endTime": end_time,
            "start": start,
            "count": 100
        }
        headers = {"X-Riot-Token": RIOT_API_KEY}
        r = requests.get(url, headers=headers, params=params)
        batch = r.json()

        if not batch:
            break

        all_ids.extend(batch)
        start += 100

    return all_ids

def get_match_details(match_id):
    url = f"https://americas.api.riotgames.com/lol/match/v5/matches/{match_id}"
    headers = {"X-Riot-Token": RIOT_API_KEY}
    r = requests.get(url, headers=headers)
    return r.json()

def get_rank_data_by_puuid(puuid):
    url = f"https://na1.api.riotgames.com/lol/league/v4/entries/by-puuid/{puuid}"
    headers = {"X-Riot-Token": RIOT_API_KEY}
    r = requests.get(url, headers=headers)
    return r.json()