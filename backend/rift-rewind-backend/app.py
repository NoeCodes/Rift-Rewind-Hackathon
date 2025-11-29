from flask import Flask, jsonify, request
from flask_cors import CORS
import logging
from services.riot_api import get_puuid, get_match_ids_last_year
from services.dashboard_service import calculate_dashboard_stats

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

logger = logging.getLogger(__name__)

@app.route('/api/player/<game_name>/<tag_line>', methods=['GET'])
def get_player_data(game_name, tag_line):
    """
    Fetch player data from Riot API and calculate dashboard stats
    """
    try:
        logger.info(f"Fetching data for player: {game_name}#{tag_line}")

        # Get PUUID
        puuid = get_puuid(game_name, tag_line)
        if not puuid:
            logger.error(f"Could not find PUUID for {game_name}#{tag_line}")
            return jsonify({
                "error": "Player not found",
                "message": f"Could not find player {game_name}#{tag_line}"
            }), 404

        logger.info(f"Found PUUID: {puuid}")

        # Get match IDs
        match_ids = get_match_ids_last_year(puuid)
        if not match_ids:
            logger.warning(f"No matches found for {game_name}#{tag_line}")
            return jsonify({
                "error": "No matches found",
                "message": "This player has no matches in 2025"
            }), 404

        logger.info(f"Found {len(match_ids)} matches")

        # Calculate dashboard stats
        stats = calculate_dashboard_stats(puuid, match_ids)

        # Add player name info to response
        stats["player_name"] = game_name
        stats["tag_line"] = tag_line
        stats["puuid"] = puuid

        logger.info("Successfully calculated player stats")
        return jsonify(stats), 200

    except Exception as e:
        logger.error(f"Error fetching player data: {str(e)}")
        return jsonify({
            "error": "Internal server error",
            "message": str(e)
        }), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy"}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
