import os
import logging
from openai import OpenAI

logger = logging.getLogger(__name__)

def generate_improvement_suggestions(player_stats):
    """
    Generate personalized improvement suggestions for a player using OpenAI API

    Args:
        player_stats: Dictionary containing player statistics including:
            - total_games: Number of games played
            - win_rate: Win rate percentage
            - hours_played: Total hours played
            - favorite_role: Most played role
            - ranked_status: Dict with tier and rank
            - top_3_champions: Dict of top champions with their stats

    Returns:
        List of improvement suggestions as strings
    """
    try:
        # Initialize OpenAI client
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            logger.error("OPENAI_API_KEY environment variable not set")
            return ["Error: OpenAI API key not configured. Please set OPENAI_API_KEY environment variable."]

        client = OpenAI(api_key=api_key)

        # Build context about the player
        top_champs_info = []
        for champ_name, champ_data in player_stats.get("top_3_champions", {}).items():
            top_champs_info.append(
                f"{champ_name}: {champ_data['games_played']} games, "
                f"{champ_data['win_rate']}% WR, {champ_data['kda']} KDA"
            )

        top_champs_str = "\n".join(top_champs_info) if top_champs_info else "No champion data available"

        ranked_status = player_stats.get("ranked_status", {})
        rank_str = f"{ranked_status.get('tier', 'Unranked')} {ranked_status.get('rank', '')}"

        prompt = f"""You are a professional League of Legends coach. Analyze the following player statistics and provide 3-5 specific, actionable improvement suggestions.

Player Stats:
- Total Games Played: {player_stats.get('total_games', 'N/A')}
- Win Rate: {player_stats.get('win_rate', 'N/A')}%
- Hours Played: {player_stats.get('hours_played', 'N/A')}
- Favorite Role: {player_stats.get('favorite_role', 'N/A')}
- Current Rank: {rank_str}

Top Champions:
{top_champs_str}

Based on these stats, provide specific advice to help this player improve. Focus on:
1. Champion pool and performance trends
2. Win rate optimization
3. Role mastery
4. Gameplay improvement areas

Format your response as a numbered list of 3-5 concise suggestions (each 1-2 sentences max)."""

        # Call OpenAI API
        logger.info("Calling OpenAI API for player improvement suggestions")
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a professional League of Legends coach providing actionable improvement advice."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,
            temperature=0.7
        )

        # Extract suggestions from response
        suggestions_text = response.choices[0].message.content
        logger.info("Successfully generated improvement suggestions")

        # Parse the numbered list into individual suggestions
        suggestions = []
        lines = suggestions_text.strip().split('\n')
        for line in lines:
            line = line.strip()
            if line and (line[0].isdigit() or line.startswith('-') or line.startswith('•')):
                # Remove numbering/bullets and clean up
                cleaned = line.lstrip('0123456789.-•) ').strip()
                if cleaned:
                    suggestions.append(cleaned)

        # If parsing failed, return raw text split by periods or newlines
        if not suggestions:
            suggestions = [s.strip() for s in suggestions_text.split('\n') if s.strip()]

        return suggestions if suggestions else ["Unable to generate suggestions at this time."]

    except Exception as e:
        logger.error(f"Error generating improvement suggestions: {str(e)}")
        return [f"Error generating suggestions: {str(e)}"]
