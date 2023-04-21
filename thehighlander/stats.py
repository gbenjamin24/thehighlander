# stats.py
# this was insanely useful! big shoutout to this dev nntrn
# https://gist.github.com/nntrn/ee26cb2a0716de0947a0a4e9a157bc1c#v2sportsfootballleaguesnflathletes
from flask import current_app
import requests, logging

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[logging.StreamHandler()])

def get_team_id(team_name):
    url = "http://site.api.espn.com/apis/site/v2/sports/basketball/nba/teams"
    response = requests.get(url)
    leagues = response.json()["sports"][0]["leagues"]

    for league in leagues:
        teams = league["teams"]
        for team_data in teams:
            team = team_data["team"]
            display_name = team["displayName"].lower()
            short_display_name = team["shortDisplayName"].lower()
            if team_name.lower() in display_name or team_name.lower() in short_display_name:
                return team["id"]

    return None

def nested_dict_to_csv(nested_dict):
    headers = ["Team", "Player", "Position"] + list(next(iter(next(iter(nested_dict.values())).values())).keys())[1:]
    rows = []
    for team, players in nested_dict.items():
        for player, stats in players.items():
            row = [team, player, stats["position"]] + [v for k, v in stats.items() if k != "position"]
            rows.append(",".join(str(x) for x in row))
    
    csv_string = ",".join(headers) + "\n" + "\n".join(rows)
    return csv_string


def get_teams_player_stats(teams):
    all_stats = {}
    
    for team_name in teams:
        team_id = get_team_id(team_name)

        if team_id is None:
            current_app.logger.info(f"Team {team_name} not found.")
            continue

        url = f"http://site.api.espn.com/apis/site/v2/sports/basketball/nba/teams/{team_id}/roster"
        response = requests.get(url)
        roster_data = response.json()

        team_stats = {}
        for player in roster_data["athletes"]:
            player_id = player["id"]
            player_name = player["fullName"]
            player_position = player["position"]["abbreviation"]

            url = f"https://site.web.api.espn.com/apis/common/v3/sports/basketball/nba/athletes/{player_id}/splits"
            response = requests.get(url)
            stats_data = response.json()

            # Find the index of the "Total" split in the splitCategories
            total_index = next((index for index, split in enumerate(stats_data["splitCategories"][0]["splits"]) if split["abbreviation"] == "Total"), None)

            if total_index is None:
                current_app.logger.info(f"Total stats not found for player {player_name}.")
                continue

            total_stats = stats_data["splitCategories"][0]["splits"][total_index]["stats"]

            # Create a dictionary with stat names and values
            player_stats = {"position": player_position}
            for stat_name, stat_value in zip(stats_data["names"], total_stats):
                player_stats[stat_name] = stat_value

            team_stats[player_name] = player_stats

        all_stats[team_name] = team_stats

    return nested_dict_to_csv(all_stats)


