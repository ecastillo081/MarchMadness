import pandas as pd
import random
import requests
import json
from credentials.token import GITHUB_TOKEN, GIST_ID

# 🔹 Update this with the actual path to your Excel file
file_path = "C:/Users/CashTO/Desktop/March Madness Randomizer.xlsx"

# 🔹 Load the Excel sheets
players_df = pd.read_excel(file_path, sheet_name="Players")  # Adjust sheet name if needed
teams_df = pd.read_excel(file_path, sheet_name="Teams")  # Adjust sheet name if needed

# Extract player names and team names
players = players_df["Player Name"].tolist()
teams = teams_df["Team Name"].tolist()

# Shuffle teams randomly
random.shuffle(teams)

# Assign teams to players
assignments = {player: [] for player in players}
for i, team in enumerate(teams):
    assignments[players[i % len(players)]].append(team)

# Convert assignments to formatted string for Gist
result_text = "\n".join([f"{player}: {', '.join(team_list)}" for player, team_list in assignments.items()])

# 🔹 GitHub API credentials
gist_url = f"https://api.github.com/gists/{GIST_ID}"
headers = {"Authorization": f"token {GITHUB_TOKEN}"}

# Prepare payload for GitHub Gist
payload = {
    "description": "March Madness Team Assignments",
    "public": True,  # Make it public so everyone can see
    "files": {"march_madness_assignments.txt": {"content": result_text}}
}

# Send request to update Gist
response = requests.patch(gist_url, headers=headers, data=json.dumps(payload))

# Output result
if response.ok:
    gist_url = response.json().get("html_url", f"https://gist.github.com/{GIST_ID}")
    print(f"✅ Assignments updated successfully!\nView here: {gist_url}")
else:
    print(f"❌ Failed to update Gist. HTTP Status: {response.status_code}\nResponse: {response.text}")
