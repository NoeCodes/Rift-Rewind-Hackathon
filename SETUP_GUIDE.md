# Rift Rewind - Setup Guide

This guide will help you set up and run the Rift Rewind application with the player search functionality connected to the Riot API.

## Prerequisites

- Python 3.8+ installed
- Node.js 18+ and npm installed
- A valid Riot API key

## Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend/rift-rewind-backend
   ```

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Make sure your Riot API key is configured in `services/riot_api.py` (line 14)

4. Run the Flask server:
   ```bash
   python app.py
   ```

   The backend API will start on `http://localhost:5000`

## Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend/rift-rewind
   ```

2. Install npm dependencies:
   ```bash
   npm install
   ```

3. Start the Angular development server:
   ```bash
   npm start
   ```
   or
   ```bash
   ng serve
   ```

   The frontend will start on `http://localhost:4200`

## Using the Application

1. Open your browser and navigate to `http://localhost:4200`

2. You'll see the search screen where you can enter a player's name and tag (e.g., "PAPA" and "sanda")

3. Click the "Continue" button to fetch the player data from Riot API

4. The application will:
   - Call the backend API at `/api/player/{name}/{tag}`
   - Fetch the player's PUUID from Riot API
   - Retrieve match history for 2025
   - Calculate dashboard statistics
   - Display the results on the dashboard page

5. The dashboard will show:
   - Player name and rank
   - Total games, win rate, favorite role, and hours played
   - Top 3 champions with stats

## Architecture

### Backend (`backend/rift-rewind-backend/`)
- `app.py` - Flask API server with endpoints
- `services/riot_api.py` - Functions to interact with Riot API
- `services/dashboard_service.py` - Business logic to calculate player stats
- `services/insight_service.py` - Additional insights processing

### Frontend (`frontend/rift-rewind/src/app/`)
- `app.ts` / `app.html` - Main app component with search screen
- `services/api.service.ts` - HTTP service to call backend API
- `services/player-data.service.ts` - Shared service to store player data
- `components/dashboard/` - Dashboard component to display player stats

## API Endpoints

### `GET /api/player/<game_name>/<tag_line>`
Fetches player data from Riot API and returns dashboard statistics.

**Response:**
```json
{
  "player_name": "PAPA",
  "tag_line": "sanda",
  "puuid": "...",
  "total_games": 123,
  "win_rate": 54.3,
  "hours_played": 45.6,
  "favorite_role": "Mid Lane",
  "ranked_status": {
    "tier": "Gold",
    "rank": "II"
  },
  "top_3_champions": {
    "Ahri": {
      "champion_name": "Ahri",
      "games_played": 25,
      "win_rate": 60.0,
      "kda": 3.4
    }
  }
}
```

### `GET /api/health`
Health check endpoint to verify the API is running.

## Notes

- The backend fetches matches in batches to avoid rate limiting
- The application currently fetches matches from 2025 (modify `start_time` in `riot_api.py` if needed)
- Make sure both backend and frontend are running simultaneously
- The frontend expects the backend to be running on `http://localhost:5000`
