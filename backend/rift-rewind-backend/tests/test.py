# Just used for local testing
# To test, cd to "rift-rewind-backend", and run "python tests/test.py" on the terminal
import sys
import os

# Add parent directory of 'tests' to Python's search path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from services.riot_api import get_puuid

# Example player
puuid = get_puuid("Nikuz", "MIKUZ")
print("PUUID:", puuid)
