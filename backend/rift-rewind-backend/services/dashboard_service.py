import services.riot_api
import time 

def calculate_dashboard_stats(puuid, match_ids):
    total_games = len(match_ids)
    wins = 0
    total_duration = 0

    batch_size = 20
    cooldown = 25 

    for i in range(0, len(match_ids), batch_size):
        batch = match_ids[i:i+batch_size]
        for mid in batch:
            match = services.riot_api.get_match_details(mid)
    
            if "status" in match:
                print(f"Error for match {mid}: {match['status']}")
                time.sleep(2)  # small delay before next request
                continue

            if "info" not in match:
                print(f"Skipping match {mid} — no 'info' field")
                time.sleep(2)
                continue
            

            participants = match["info"]["participants"]
            player = next(p for p in participants if p["puuid"] == puuid)

            if player["win"]:
                wins += 1
            total_duration += match["info"]["gameDuration"]
        
        print(f"Finished batch {i // batch_size + 1}, cooling down...")
        time.sleep(cooldown)

    if total_games == 0:
        return {"total_games": 0, "win_rate": 0.0, "hours_played": 0.0}

    win_rate = round((wins / total_games) * 100, 1)
    hours_played = round(total_duration / 3600, 1)

    return {
        "total_games": total_games,
        "win_rate": win_rate,
        "hours_played": hours_played
    }

# I still need to fix this -Noe
def ranked_status(puuid):
    ranked_data = services.riot_api.get_rank_data_by_puuid(puuid)
    tier = ranked_data[0]["tier"]
    rank = ranked_data[0]["rank"]
    return {
        "tier": tier,
        "rank": rank,
    }