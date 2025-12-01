import logging
from pymongo import MongoClient
from datetime import datetime

logger = logging.getLogger(__name__)

# MongoDB Atlas connection URI
MONGO_URI = "mongodb+srv://BigData:pEG9cjByK4E0qcxD@bigdata.ouly8yn.mongodb.net/BigData?retryWrites=true&w=majority&appName=BigData"

# Global MongoDB client
_mongo_client = None
_db = None
_connection_failed = False

def get_database():
    """
    Get MongoDB database instance
    Returns the database connection, creating it if it doesn't exist
    Returns None if connection fails (allows app to continue without DB)
    """
    global _mongo_client, _db, _connection_failed

    # If we already know connection failed, don't retry constantly
    if _connection_failed:
        return None

    if _db is None:
        try:
            logger.info("Connecting to MongoDB...")
            _mongo_client = MongoClient(
                MONGO_URI,
                serverSelectionTimeoutMS=5000,  # 5 second timeout
                connectTimeoutMS=5000
            )
            _db = _mongo_client["BigData"]
            # Test the connection
            _mongo_client.admin.command('ping')
            logger.info("Successfully connected to MongoDB")
        except Exception as e:
            logger.error(f"Failed to connect to MongoDB: {str(e)}")
            logger.warning("App will continue without database caching")
            _connection_failed = True
            return None

    return _db

def close_database():
    """
    Close MongoDB connection
    """
    global _mongo_client, _db

    if _mongo_client:
        _mongo_client.close()
        _mongo_client = None
        _db = None
        logger.info("MongoDB connection closed")

def save_player(game_name, tag_line, puuid):
    """
    Save or update player information

    Args:
        game_name: Player's game name
        tag_line: Player's tag line
        puuid: Player's PUUID
    """
    try:
        db = get_database()
        if db is None:
            logger.warning("Database not available, skipping player save")
            return

        players_collection = db["players"]

        player_data = {
            "game_name": game_name,
            "tag_line": tag_line,
            "puuid": puuid,
            "last_updated": datetime.utcnow()
        }

        # Upsert: update if exists, insert if not
        players_collection.update_one(
            {"puuid": puuid},
            {"$set": player_data},
            upsert=True
        )
        logger.info(f"Saved player data for {game_name}#{tag_line}")
    except Exception as e:
        logger.error(f"Error saving player data: {str(e)}")
        # Don't raise - allow app to continue

def get_player(puuid):
    """
    Get player information by PUUID

    Args:
        puuid: Player's PUUID

    Returns:
        Player document or None if not found
    """
    try:
        db = get_database()
        if db is None:
            return None

        players_collection = db["players"]
        return players_collection.find_one({"puuid": puuid})
    except Exception as e:
        logger.error(f"Error getting player data: {str(e)}")
        return None

def save_match(match_data):
    """
    Save match data to database

    Args:
        match_data: Complete match data from Riot API
    """
    try:
        db = get_database()
        if db is None:
            logger.warning("Database not available, skipping match save")
            return

        matches_collection = db["matches"]

        match_id = match_data["metadata"]["matchId"]
        match_data["saved_at"] = datetime.utcnow()

        # Upsert: update if exists, insert if not
        matches_collection.update_one(
            {"metadata.matchId": match_id},
            {"$set": match_data},
            upsert=True
        )
        logger.info(f"Saved match data for {match_id}")
    except Exception as e:
        logger.error(f"Error saving match data: {str(e)}")
        # Don't raise - allow app to continue

def get_match(match_id):
    """
    Get match data by match ID

    Args:
        match_id: Match ID

    Returns:
        Match document or None if not found
    """
    try:
        db = get_database()
        if db is None:
            return None

        matches_collection = db["matches"]
        return matches_collection.find_one({"metadata.matchId": match_id})
    except Exception as e:
        logger.error(f"Error getting match data: {str(e)}")
        return None

def save_player_stats(puuid, stats):
    """
    Save calculated player statistics

    Args:
        puuid: Player's PUUID
        stats: Dictionary of calculated statistics
    """
    try:
        db = get_database()
        if db is None:
            logger.warning("Database not available, skipping stats save")
            return

        stats_collection = db["player_stats"]

        stats_data = {
            "puuid": puuid,
            "stats": stats,
            "calculated_at": datetime.utcnow()
        }

        # Upsert: update if exists, insert if not
        stats_collection.update_one(
            {"puuid": puuid},
            {"$set": stats_data},
            upsert=True
        )
        logger.info(f"Saved player stats for {puuid}")
    except Exception as e:
        logger.error(f"Error saving player stats: {str(e)}")
        # Don't raise - allow app to continue

def get_player_stats(puuid):
    """
    Get cached player statistics

    Args:
        puuid: Player's PUUID

    Returns:
        Stats document or None if not found
    """
    try:
        db = get_database()
        if db is None:
            return None

        stats_collection = db["player_stats"]
        return stats_collection.find_one({"puuid": puuid})
    except Exception as e:
        logger.error(f"Error getting player stats: {str(e)}")
        return None

def get_player_matches(puuid, limit=10):
    """
    Get matches for a specific player from database

    Args:
        puuid: Player's PUUID
        limit: Maximum number of matches to return

    Returns:
        List of match documents
    """
    try:
        db = get_database()
        if db is None:
            return []

        matches_collection = db["matches"]

        # Find matches where the player's PUUID appears in participants
        matches = matches_collection.find(
            {"info.participants.puuid": puuid}
        ).sort("info.gameCreation", -1).limit(limit)

        return list(matches)
    except Exception as e:
        logger.error(f"Error getting player matches: {str(e)}")
        return []
