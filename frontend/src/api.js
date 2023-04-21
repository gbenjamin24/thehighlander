const API_BASE_URL = "/api";

export async function fetchWeeklyBasketballGames() {
  const response = await fetch(`${API_BASE_URL}/weekly_basketball_games`);
  return response.json();
}

export async function suggestTeam(game) {
  const response = await fetch(`${API_BASE_URL}/suggest_team`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(game),
  });
  const suggestedTeam = await response.json();
  return (`${suggestedTeam.team_name}`);
}