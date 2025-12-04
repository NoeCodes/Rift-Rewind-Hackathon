import json
import os
from datetime import datetime
from collections import defaultdict, Counter

# Keeps running champion counts per player across many matches
_champion_counts = defaultdict(Counter)

def receive_match_json(match_json, puuid):
    match_id = match_json.get("metadata", {}).get("matchId", "UNKNOWN_MATCH")
    print(f"[insight_service] Received game: {match_id} for puuid={puuid}")

    _accumulate_champion_for_player(match_json, puuid)


def _accumulate_champion_for_player(match_json, puuid):
    """
    Find the participant for this puuid in the match JSON and record championName.
    Expected structure (success case):
      match_json["info"]["participants"] -> list of 10 dicts, each with "puuid" and "championName".
    Safely no-ops if structure is missing.
    """
    info = match_json.get("info")
    if not info:
        print("[insight_service] No 'info' in match JSON; skipping accumulation.")
        return

    participants = info.get("participants", [])
    if not isinstance(participants, list) or not participants:
        print("[insight_service] No 'participants' list in 'info'; skipping accumulation.")
        return

    player = next((p for p in participants if p.get("puuid") == puuid), None)
    if not player:
        print(f"[insight_service] PUUID {puuid} not found among participants; skipping.")
        return

    champ = player.get("championName")
    if not champ:
        print(f"[insight_service] No 'championName' for puuid={puuid} in this match; skipping.")
        return

    champ_norm = champ.strip()
    _champion_counts[puuid][champ_norm] += 1


def get_most_played_champion(puuid, top_n=3):
    """
    Returns a list of (championName, count) sorted by count desc for this puuid.
    Example: [('Ahri', 5), ('Lux', 3), ('Ezreal', 2)]
    """
    counter = _champion_counts.get(puuid)
    if not counter:
        return []
    return counter.most_common(top_n)


def reset_champion_counts(puuid=None):
    if puuid is None:
        _champion_counts.clear()
    else:
        _champion_counts.pop(puuid, None)