import services.riot_api
import time 
import logging

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
    matches = []    # List of all matches data
    batch_size = 20
    cooldown = 25 

    for i in range(0, len(match_ids), batch_size):
        batch = match_ids[i:i+batch_size]
        for mid in batch:
            match = services.riot_api.get_match_details(mid)
            if "status" in match:
                logger.warning(f"Error for match {mid}: {match['status']}")
                time.sleep(2)  # small delay before next request
                continue

            if "info" not in match:
                logger.warning(f"Skipping match {mid} — no 'info' field")
                time.sleep(2)
                continue
            
            matches.append(match)
            
        logger.info(f"Finished batch {i // batch_size + 1}, cooling down...")
        time.sleep(cooldown)

    total_games = len(matches)
    win_rate = get_win_rate(puuid, matches)
    hours_played = get_hours_played(puuid, matches)
    favorite_role = get_favorite_role(puuid, matches)
    ranked_info = ranked_status(puuid)
    logger.info("Calculating dashboard stats successful.")

    return {
        "total_games": total_games,
        "win_rate": win_rate,
        "hours_played": hours_played,
        "favorite_role": favorite_role,
        "ranked_status": ranked_info
    }