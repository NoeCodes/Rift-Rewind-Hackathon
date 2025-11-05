# Just used for local testing (AWS handles paths on the cloud)
# To test, cd to "rift-rewind-backend", and run "python tests/test.py" on the terminal
# To test a function, change the function call in __main__

import sys
import os

# Add parent directory of 'tests' to Python's search path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from services.riot_api import get_puuid
from services.riot_api import get_match_ids_last_year
from services.dashboard_service import calculate_dashboard_stats
from services.insight_service import get_most_played_champion

def get_puuid_test():
    # Example player
    puuid = get_puuid("Nikuz", "MIKUZ")
    print("PUUID:", puuid)

def calculate_dashboard_stats_test():
    game_name = "Nikuz"
    tag_line = "MIKUZ"

    print("Running Dashboard Stats Test...")
    try:
        stats = calculate_dashboard_stats(game_name, tag_line)
        print("✅ Stats calculated successfully:")
        print(stats)

        # Optional assertions (basic checks)
        assert "total_games" in stats
        assert "win_rate" in stats
        assert "hours_played" in stats
        print("Basic checks passed.")

    except Exception as e:
        print("Test failed with error:", e)
        
# Use any function here to test
if __name__ == "__main__":
    puuid = get_puuid("PAPA", "sanda") #Mugi ツ#wara, YorozuyaSho#0725
    match_ids = get_match_ids_last_year(puuid)
    stats = calculate_dashboard_stats(puuid, match_ids)
    print(stats)
    print(puuid)
    print(get_most_played_champion(puuid, top_n=5))