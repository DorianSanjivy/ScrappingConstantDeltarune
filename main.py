import json
import requests
from bs4 import BeautifulSoup
from time import sleep
import json
from datetime import datetime
import time


def scrape_data(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    players = int(soup.select_one("#TotalPlayers")['data-val'])
    plays = int(soup.select_one("#TotalPlays")['data-val'])
    active_users = int(soup.select_one("#ActiveUsers")['data-val'])

    return players, plays, active_users

def get_data():
    return scrape_data('https://www.construct.net/en/free-online-games/deltarune-dreamland-saga-42306/play?via=pp')

def save_to_json(data):
    # Chargez les données existantes
    try:
        with open('data.json', 'r', encoding='utf-8') as f:
            existing_data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        existing_data = []

    # Ajoutez les nouvelles données avec un timestamp, à l'extérieur du bloc except
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    data["timestamp"] = timestamp
    existing_data.append(data)

    # Sauvegardez les données mises à jour
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(existing_data, f, ensure_ascii=False, indent=4)

while True:
    players, plays, active_users = get_data()

    # Save data to JSON
    data = {
        "players": players,
        "plays": plays,
        "active_users": active_users
    }
    save_to_json(data)

    time.sleep(60)
