import services.riot_api
import time
import logging
import json
import os
import services.insight_service as insight_service

logger = logging.getLogger(__name__)

def ranked_status(puuid):
    ranked_data = services.riot_api.get_rank_data_by_puuid(puuid)
    tier = "Unranked"
    rank = "Unranked"

    if not ranked_data:
        logger.warning("ranked_data is empty.")
    elif ranked_data[0].get("queueType") != "RANKED_SOLO_5x5":
        logger.warning("RANKED_SOLO_5x5 not found in first entry.")
    else:
        tier = ranked_data[0]["tier"]
        rank = ranked_data[0]["rank"]
        logger.info("Ranked status found successfully.")

    return {
            "tier": tier,
            "rank": rank
        }

def get_favorite_role(puuid, matches):
    role_counts = {}
    for match in matches:
        player = next((p for p in match["info"]["participants"] if p["puuid"] == puuid), None)
        if not player:
            logger.warning("Player's PUUID not found in list of matches.")
            continue
        role = player.get("teamPosition", "UNKNOWN")
        role_counts[role] = role_counts.get(role, 0) + 1

    if not role_counts:
        logger.warning("role_counts is empty.")
        return "Unknown"

    most_played_role = max(role_counts, key=role_counts.get)

    role_map = {
        "TOP": "Top Lane",
        "JUNGLE": "Jungle",
        "MIDDLE": "Mid Lane",
        "BOTTOM": "Bot Lane",
        "UTILITY": "Support",
        "UNKNOWN": "Unknown"
    }
    return role_map.get(most_played_role, "Unknown")

def get_win_rate(puuid, matches):
    total_wins = 0
    total_games = len(matches)
    for match in matches:
        player = next((p for p in match["info"]["participants"] if p["puuid"] == puuid), None)
        if not player:
            logger.warning("Player's PUUID not found in list of matches.")
            continue
        if player["win"]:
            total_wins += 1
    win_rate = round((total_wins / total_games) * 100, 1)
    return win_rate

def get_hours_played(puuid, matches):
    total_duration = 0
    for match in matches:
        player = next((p for p in match["info"]["participants"] if p["puuid"] == puuid), None)
        if not player:
            logger.warning("Player's PUUID not found in list of matches.")
            continue
        total_duration += match["info"]["gameDuration"]
    hours_played = round(total_duration / 3600, 1)
    return hours_played


def calculate_dashboard_stats(puuid, match_ids):
    """
    Calculate dashboard statistics from match data

    Args:
        puuid: Player's PUUID
        match_ids: List of match IDs to process

    Returns:
        Dictionary with dashboard statistics
    """
    matches = []

    logger.info(f"Processing {len(match_ids)} matches...")

    for mid in match_ids:
        match = services.riot_api.get_match_details(mid)

        insight_service.receive_match_json(match, puuid)

        if "status" in match:
            logger.warning(f"Error for match {mid}: {match['status']}")
            continue

        if "info" not in match:
            logger.warning(f"Skipping match {mid} — no 'info' field")
            continue

        matches.append(match)

    logger.info(f"Successfully processed {len(matches)} matches")

    total_games = len(matches)
    win_rate = get_win_rate(puuid, matches)
    hours_played = get_hours_played(puuid, matches)
    favorite_role = get_favorite_role(puuid, matches)
    ranked_info = ranked_status(puuid)
    top_3_champions = get_top_champions_preview(puuid, matches)
    logger.info("Calculating dashboard stats successful.")

    return {
        "total_games": total_games,
        "win_rate": win_rate,
        "hours_played": hours_played,
        "favorite_role": favorite_role,
        "ranked_status": ranked_info,
        "top_3_champions": top_3_champions
    }
    

def get_top_champions_preview(puuid, matches):
    top_champions = services.riot_api.get_champions_mastery(puuid)
    if not top_champions:
        logger.warning("No champion mastery data returned for this player.")
        return {}

    top_3_champions = top_champions[:3]

    # Use relative path to champions.json
    current_dir = os.path.dirname(os.path.abspath(__file__))
    champions_json_path = os.path.join(current_dir, "..", "data", "champions.json")

    with open(champions_json_path) as f:
        champion_map = json.load(f)
    
    top_3_champions_dict = {}
    for champ in top_3_champions:
        champ_id = str(champ["championId"])
        champ_name = champion_map.get(champ_id, "Unknown")
        games_played = 0
        win_rate = 0.0
        total_wins = 0
        total_kda = 0.0
        games_played = 0
        average_kda = 0.0
        if champ_name != "Unknown":
            champ_initial = champ_name[0]
        else:
            champ_initial = "?"
            
        # Nested loop to calculate win_rate and kda for each champion
        for match in matches:
            player = next((p for p in match["info"]["participants"] if p["puuid"] == puuid), None)
            if not player:
                logger.warning(f"Skipping match {match.get('metadata', {}).get('matchId', 'unknown')} — player not found.")
                continue
            player_challenge = player["challenges"]
            if player["championName"] != champ_name:
                continue
            games_played += 1
            if player["win"]:
                total_wins += 1
            total_kda += player_challenge.get("kda", 0.0)
            
        if games_played != 0:
            win_rate = round((total_wins / games_played) * 100, 1)
            average_kda = round((total_kda / games_played) * 100, 1)
        else:
            logger.warning(f"{champ_name} had 0 games played in match data.")
            win_rate = 0.0
            average_kda = 0.0
            
            
        

        top_3_champions_dict[champ_name] = {
            "champion_name": champ_name,
            "champion_initial": champ_initial,
            "games_played": games_played,
            "win_rate": win_rate,
            "kda": average_kda
        }

    return top_3_champions_dict
    
def get_champion_name(champion_id):
    return champion_map.get(str(champion_id), "Unknown")