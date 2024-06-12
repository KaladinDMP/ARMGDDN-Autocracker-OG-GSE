import requests
import json
import nltk
import os
import datetime
import time
import sys
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

nltk.download('punkt')
nltk.download('stopwords')

def get_executable_path():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    else:
        return os.path.dirname(os.path.abspath(__file__))

def get_file_path(filename):
    return os.path.join(get_executable_path(), filename)
    
def preprocess_game_name(game_name):
    if not isinstance(game_name, str):
        return ""
    game_name = ''.join(char for char in game_name if char.isalnum() or char.isspace())
    tokens = word_tokenize(game_name)
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [word.lower() for word in tokens if word.isalnum() and word.lower() not in stop_words]
    return ' '.join(filtered_tokens)

def download_app_list(since=0):
    url = f"https://api.steampowered.com/ISteamApps/GetAppList/v2/?since={since}"
    response = requests.get(url)
    if response.status_code == 200:
        data = json.loads(response.text)
        app_list = data['applist']['apps']
        print(f"Downloaded {len(app_list)} new apps.")
        return app_list
    else:
        print(f"Error: {response.status_code}")
        return None

def create_app_dict(app_list, non_game_apps, app_dict=None):
    if app_dict is None:
        app_dict = {}
    total_apps = len(app_list)
    print(f"Downloading app dictionary for {total_apps} apps. Please wait...")

    for i, app in enumerate(app_list, start=1):
        app_id = str(app.get('appid'))
        game_name = app.get('name')
        if app_id and game_name and app_id not in non_game_apps:
            processed_name = preprocess_game_name(game_name)
            app_dict[app_id] = {'original_name': game_name, 'processed_name': processed_name}
        
        if i % 20000 == 0:
            print(f"Processed {i} out of {total_apps} apps...")
    
    print("App dictionary downloaded successfully.")
    return app_dict

def write_steam_appid_file(app_id):
    filename = get_file_path("steam_appid.txt")
    with open(filename, 'w') as file:
        file.write(str(app_id))
    print(f"steam_appid.txt file created with App ID: {app_id}")

def save_app_dict(app_dict):
    filename = get_file_path("steam_app_dict.json")
    with open(filename, 'w') as file:
        json.dump(app_dict, file)

def load_app_dict():
    filename = get_file_path("steam_app_dict.json")
    app_dict = {}
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            app_dict_data = json.load(file)
            for app_id, app_data in app_dict_data.items():
                app_dict[app_id] = {
                    'original_name': app_data['original_name'],
                    'processed_name': app_data['processed_name']
                }
    else:
        print(f"{filename} not found.")
    return app_dict

def save_non_game_apps(non_game_apps):
    filename = get_file_path("non_game_apps.json")
    with open(filename, 'w') as file:
        json.dump(list(non_game_apps), file)

def load_non_game_apps():
    filename = get_file_path("non_game_apps.json")
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            try:
                non_game_apps = set(str(app_id) for app_id in json.load(file))
                return non_game_apps
            except json.JSONDecodeError:
                print("Error: Invalid JSON data in non_game_apps.json file.")
                return set()
    else:
        return set()

def is_game(app_id):
    url = f"https://store.steampowered.com/api/appdetails?appids={app_id}"
    response = requests.get(url)
    if response.status_code == 200:
        data = json.loads(response.text)
        if str(app_id) in data and data[str(app_id)]['success']:
            return data[str(app_id)]['data']['type'] == 'game'
    return False

def search_games(game_name, app_dict, non_game_apps):
    processed_name = preprocess_game_name(game_name)
    matching_games = []

    for app_id, app_data in app_dict.items():
        processed_game_name = app_data['processed_name']
        if app_id not in non_game_apps and processed_name in processed_game_name.lower():
            matching_games.append((app_id, app_data['original_name']))

    return matching_games

def remove_non_games(matching_games, non_game_apps):
    updated_matching_games = []
    for app_id, game_name in matching_games:
        if not is_game(app_id):
            non_game_apps.add(app_id)
        else:
            updated_matching_games.append((app_id, game_name))
    return updated_matching_games, non_game_apps
    
def save_last_update_timestamp(timestamp):
    filename = get_file_path("last_update_timestamp.txt")
    with open(filename, 'w') as file:
        file.write(str(timestamp))
    
def load_last_update_timestamp():
    filename = get_file_path("last_update_timestamp.txt")
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            return float(file.read())
    return 0

print("Loading app dictionary...")
app_dict = load_app_dict()
print("App dictionary loaded.")

print("Loading non-game app IDs...")
non_game_apps = load_non_game_apps()
print("Non-game app IDs loaded.")

print("Checking for updates...")
last_update_timestamp = load_last_update_timestamp()

current_timestamp = time.time()
if current_timestamp - last_update_timestamp >= 24 * 60 * 60:
    print("Downloading new app entries from Steam...")
    new_apps = download_app_list(since=int(last_update_timestamp))
    if new_apps is not None:
        print(f"Found {len(new_apps)} new app entries.")
        print("Updating app dictionary...")
        app_dict = create_app_dict(new_apps, non_game_apps, app_dict)
        print("Saving app dictionary...")
        save_app_dict(app_dict)
        save_last_update_timestamp(current_timestamp)
        print("App dictionary updated successfully.")
    else:
        print("Failed to download new app entries.")
else:
    print("App dictionary is up to date.")

if app_dict:
    while True:
        game_name = input("Enter the game name (or 'x' to exit): ")
        if game_name.lower() == 'x':
            print("Exiting the script.")
            break
        
        print("Searching for matching games...")
        matching_games = search_games(game_name, app_dict, non_game_apps)
        
        if matching_games:
            print("Checking if the matching games are actual games...")
            updated_matching_games, non_game_apps = remove_non_games(matching_games, non_game_apps)
            
            if updated_matching_games:
                print("Matching games found:")
                for index, (app_id, game_name) in enumerate(updated_matching_games, start=1):
                    print(f"{index}. App ID: {app_id}, Game Name: {game_name}")
                
                print(f"{len(updated_matching_games) + 1}. None of these are right, try again")
                print(f"{len(updated_matching_games) + 2}. None of these are right, quit and enter manually")
                
                while True:
                    selection = input("Enter the number of the correct game: ")
                    
                    try:
                        selection = int(selection)
                        if 1 <= selection <= len(updated_matching_games):
                            selected_app_id, selected_game_name = updated_matching_games[selection - 1]
                            print(f"Selected Game: App ID: {selected_app_id}, Game Name: {selected_game_name}")
                            write_steam_appid_file(selected_app_id)
                            save_non_game_apps(non_game_apps)
                            print("Exiting the script.")
                            sys.exit(0)
                        elif selection == len(updated_matching_games) + 1:
                            print("None of these are right. I want to try to search again")
                            break
                        elif selection == len(updated_matching_games) + 2:
                            print("None of these are right. I want to quit and just enter the appid manually.")
                            sys.exit(0)
                        else:
                            print("Invalid selection. Please try again.")
                    except ValueError:
                        print("Invalid input. Please enter a valid number.")
            else:
                print("No matching games found.")
        else:
            print("No matching games found.")
        
        print()

print("Saving non-game app IDs...")
save_non_game_apps(non_game_apps)
print("Exiting the script.")
sys.exit(0)