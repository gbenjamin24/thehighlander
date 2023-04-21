from flask import Blueprint, jsonify
import os, requests, random, datetime

api = Blueprint("api", __name__)

@api.route("/basketball_games")
def basketball_games():
    # Fetch basketball games from the Odds API or any other source
    # Example using Odds API
    odds_api_key = os.environ.get("ODDS_API_KEY")
    odds_api_url = f"https://api.the-odds-api.com/v4/sports/basketball/odds?regions=us&apiKey={odds_api_key}"
    response = requests.get(odds_api_url)

    if response.status_code == 200:
        games = response.json()
        return jsonify(games)
    else:
        return jsonify({"error": "Unable to fetch basketball games"}), 500
    
@api.route("/weekly_basketball_games")
def weekly_basketball_games():
    # Example response format:
    # [
    #   {
    #     "home_team": {
    #       "name": "Los Angeles Lakers",
    #       "logo_url": "https://a.espncdn.com/i/teamlogos/nba/500/lal.png"
    #     },
    #     "away_team": {
    #       "name": "Golden State Warriors",
    #       "logo_url": "https://a.espncdn.com/i/teamlogos/nba/500/gs.png"
    #     },
    #     "date": "2023-04-25T02:00Z"
    #   },
    #   {
    #     "home_team": {
    #       "name": "Brooklyn Nets",
    #       "logo_url": "https://a.espncdn.com/i/teamlogos/nba/500/bkn.png"
    #     },
    #     "away_team": {
    #       "name": "Philadelphia 76ers",
    #       "logo_url": "https://a.espncdn.com/i/teamlogos/nba/500/phi.png"
    #     },
    #     "date": "2023-04-25T23:00Z"
    #   },
    #   ...
    # ]
    
    # Calculate date range for next 7 days
    start_date = datetime.date.today()
    end_date = start_date + datetime.timedelta(days=7)
    date_range = f"{start_date:%Y%m%d}-{end_date:%Y%m%d}"
    
    # Make API request to ESPN API
    url = f"http://site.api.espn.com/apis/site/v2/sports/basketball/nba/scoreboard?dates={date_range}"
    response = requests.get(url)
    response.raise_for_status()
    
    # Parse game data from API response
    games = []
    scoreboard = response.json()["events"]
    for game in scoreboard:
        home_team = game["competitions"][0]["competitors"][0]
        away_team = game["competitions"][0]["competitors"][1]
        game_data = {
            "home_team": {
                "name": home_team["team"]["name"],
                "logo_url": home_team["team"]["logo"]
            },
            "away_team": {
                "name": away_team["team"]["name"],
                "logo_url": away_team["team"]["logo"]
            },
            "date": game["date"]
        }
        games.append(game_data)
    
    # Return game data as JSON response
    return jsonify(games)


@api.route("/suggest_team", methods=["POST"])
def suggest_team():
    teams = [
        "Los Angeles Lakers",
        "Boston Celtics",
        "Golden State Warriors",
        "Chicago Bulls",
        "San Antonio Spurs",
    ]
    suggested_team = random.choice(teams)
    return jsonify({"team_name": suggested_team})