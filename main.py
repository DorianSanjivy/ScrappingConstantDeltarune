import requests
from bs4 import BeautifulSoup
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials


def scrape_data(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    players = int(soup.select_one("#TotalPlayers")['data-val'])
    plays = int(soup.select_one("#TotalPlays")['data-val'])
    active_users = int(soup.select_one("#ActiveUsers")['data-val'])

    return players, plays, active_users


def get_data():
    return scrape_data('https://www.construct.net/en/free-online-games/deltarune-dreamland-saga-42306/play?via=pp')


def save_to_google_sheets(data):
    # Authentification
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    credentials = ServiceAccountCredentials.from_json_keyfile_name("ageless-union-400617-cb593b8312e6.json", scope)
    client = gspread.authorize(credentials)

    # Ouvrir la feuille de calcul et écrire des données
    sheet = client.open("DumpDeltarune").sheet1

    row = [data["timestamp"], data["players"], data["plays"], data["active_users"]]
    sheet.append_row(row)


players, plays, active_users = get_data()

# Prepare data
timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
data = {
    "timestamp": timestamp,
    "players": players,
    "plays": plays,
    "active_users": active_users
}

# Save data to Google Sheets
save_to_google_sheets(data)
