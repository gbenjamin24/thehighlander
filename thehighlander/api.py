from flask import Blueprint, jsonify, request, current_app
import os, requests, random, datetime, logging, openai, json
from .stats import get_teams_player_stats

api = Blueprint("api", __name__)

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[logging.StreamHandler()])

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

    game_data = request.get_json()
    # current_app.logger.info(f"Received game data: {game_data}")

    teams = [
        game_data['home_team']['name'],
        game_data['away_team']['name']
    ]
    player_stats = get_teams_player_stats(teams)
    # current_app.logger.info(f"gathered stats data: {player_stats}")
    try:
        openai.api_key = os.environ.get("OPENAI_API_KEY")
        # Create a prompt for the OpenAI API
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": 'you are helping a developer with a open source webapp this webapp leverages open ai to consider the stats of all players on 2 competing BASKETBALL teams and uses these stats to offer a potential winner... lets try it out Ill give you the stats and you return me a json with a key for the potential winning team based on stats this key should be labeled "winner"  you should also return a key "confidence" which is the likelihood your winner key is correct and a key "explanation" which explains what you saw significant affecting your guess in the statistics. YOU SHOULD ONLY ANSER IN JSON FORMAT!'},
                {"role": "user", "content": f"{player_stats}"}
            ]
        )
        message_content = response.choices[0].message['content']
        # current_app.logger.info(f"openai output: {response}")
        # prediction = extract_json_from_message(message_content)
        ai_guess=json.loads(message_content)
        # current_app.logger.info(f"openai output: {json.loads(message_content)}")
        suggested_team = ai_guess['winner']
        confidence = "{:.0%}".format(ai_guess['confidence'])
        reason = ai_guess['explanation']
    except:
        suggested_team = random.choice(teams)
        confidence = "0%"
        reason = "N/A"
        
    
    return jsonify({"team_name": suggested_team, "confidence": confidence, "reason": reason})