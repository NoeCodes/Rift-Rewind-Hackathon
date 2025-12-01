import os
import requests
from dotenv import load_dotenv
from datetime import datetime
import logging
logging.basicConfig(
    level=logging.INFO,  # controls which messages show (DEBUG, INFO, WARNING, ERROR)
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)

# Load environment variables from .env
load_dotenv()

# ⚠️ UPDATE THIS DAILY - Riot dev API keys expire after 24 hours
# Get a new key from: https://developer.riotgames.com/
RIOT_API_KEY = "RGAPI-b20ec29d-cc46-4fc2-91d6-0889cd2a675f"  # Replace with your current API key

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

def get_match_ids_last_year(puuid, count=10):
    """
    Fetch recent match IDs for a player

    Args:
        puuid: Player's PUUID
        count: Number of recent matches to fetch (default: 10)

    Returns:
        List of match IDs
    """
    url = f"https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids"
    params = {
        "start": 0,
        "count": count
    }
    headers = {"X-Riot-Token": RIOT_API_KEY}
    r = requests.get(url, headers=headers, params=params)

    if r.status_code != 200:
        print(f"Error fetching match IDs: {r.status_code}")
        return []

    return r.json()

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

def get_champions_mastery(puuid):
    url = f"https://na1.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-puuid/{puuid}"
    headers = {"X-Riot-Token": RIOT_API_KEY}
    r = requests.get(url, headers=headers)
    return r.json()