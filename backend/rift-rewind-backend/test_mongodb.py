"""
Quick test script to verify MongoDB Atlas connection and operations
"""
import sys
import logging
from services.database import get_database, save_player, get_player, save_player_stats, get_player_stats

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)

logger = logging.getLogger(__name__)

def test_mongodb_connection():
    """Test MongoDB Atlas connection and basic operations"""

    print("\n" + "="*60)
    print("Testing MongoDB Atlas Connection")
    print("="*60 + "\n")

    # Test 1: Connection
    print("Test 1: Connecting to MongoDB Atlas...")
    db = get_database()
    if db is None:
        print("[FAILED] Could not connect to MongoDB")
        return False
    print("[SUCCESS] Connected to MongoDB Atlas")
    print(f"  Database: {db.name}")

    # Test 2: Save player
    print("\nTest 2: Saving player data...")
    test_puuid = "test-puuid-12345"
    save_player("TestPlayer", "NA1", test_puuid)
    print("[SUCCESS] Player data saved")

    # Test 3: Retrieve player
    print("\nTest 3: Retrieving player data...")
    player = get_player(test_puuid)
    if player:
        print("[SUCCESS] Player data retrieved")
        print(f"  Game Name: {player['game_name']}")
        print(f"  Tag Line: {player['tag_line']}")
        print(f"  PUUID: {player['puuid']}")
    else:
        print("[FAILED] Could not retrieve player data")
        return False

    # Test 4: Save stats
    print("\nTest 4: Saving player stats...")
    test_stats = {
        "total_games": 100,
        "win_rate": 55.5,
        "hours_played": 50.0,
        "favorite_role": "Mid Lane"
    }
    save_player_stats(test_puuid, test_stats)
    print("[SUCCESS] Player stats saved")

    # Test 5: Retrieve stats
    print("\nTest 5: Retrieving player stats...")
    stats_doc = get_player_stats(test_puuid)
    if stats_doc and "stats" in stats_doc:
        print("[SUCCESS] Player stats retrieved")
        print(f"  Total Games: {stats_doc['stats']['total_games']}")
        print(f"  Win Rate: {stats_doc['stats']['win_rate']}%")
    else:
        print("[FAILED] Could not retrieve player stats")
        return False

    # Test 6: List collections
    print("\nTest 6: Checking database collections...")
    collections = db.list_collection_names()
    print("[SUCCESS] Collections created")
    print(f"  Collections: {collections}")

    print("\n" + "="*60)
    print("All Tests Passed! MongoDB Atlas is working correctly!")
    print("="*60 + "\n")

    return True

if __name__ == "__main__":
    success = test_mongodb_connection()
    sys.exit(0 if success else 1)
