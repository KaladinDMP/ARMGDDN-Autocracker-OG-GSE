import requests
import json
import os
import time
import sys


def get_executable_path():
    """Return the folder where the EXE / script is running from."""
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    else:
        return os.path.dirname(os.path.abspath(__file__))


def get_file_path(filename):
    """Get a path to a file in the same folder as the EXE / script."""
    return os.path.join(get_executable_path(), filename)


def preprocess_game_name(game_name):
    """Lightweight cleaner. Should match how names are stored in steam_app_dict.json."""
    if not isinstance(game_name, str):
        return ""
    # Keep only alphanumeric + space
    cleaned = ''.join(char for char in game_name if char.isalnum() or char.isspace())
    cleaned = cleaned.lower().strip()

    # Simple stopword removal, same style as the updater
    stop_words = {"the", "a", "an", "of", "and", "in", "for", "to"}
    tokens = cleaned.split()
    filtered_tokens = [t for t in tokens if t not in stop_words]

    return " ".join(filtered_tokens)


def write_steam_appid_file(app_id):
    filename = get_file_path("steam_appid.txt")
    with open(filename, 'w', encoding="utf-8") as file:
        file.write(str(app_id))
    print(f"steam_appid.txt file created with App ID: {app_id}")


def save_app_dict(app_dict):
    filename = get_file_path("steam_app_dict.json")
    with open(filename, 'w', encoding="utf-8") as file:
        json.dump(app_dict, file)


def load_app_dict():
    filename = get_file_path("steam_app_dict.json")
    app_dict = {}
    if os.path.exists(filename):
        try:
            with open(filename, 'r', encoding="utf-8") as file:
                app_dict_data = json.load(file)
                for app_id, app_data in app_dict_data.items():
                    app_dict[app_id] = {
                        'original_name': app_data['original_name'],
                        'processed_name': app_data['processed_name']
                    }
        except (json.JSONDecodeError, OSError) as e:
            print(f"Error loading {filename}: {e}")
    else:
        print(f"{filename} not found.")
    return app_dict


def save_non_game_apps(non_game_apps):
    filename = get_file_path("non_game_apps.json")
    with open(filename, 'w', encoding="utf-8") as file:
        json.dump(list(non_game_apps), file)


def load_non_game_apps():
    filename = get_file_path("non_game_apps.json")
    if os.path.exists(filename):
        try:
            with open(filename, 'r', encoding="utf-8") as file:
                non_game_apps = set(str(app_id) for app_id in json.load(file))
                return non_game_apps
        except json.JSONDecodeError:
            print("Error: Invalid JSON data in non_game_apps.json file.")
            return set()
        except OSError as e:
            print(f"Error reading non_game_apps.json: {e}")
            return set()
    else:
        return set()


def update_app_dict_from_github():
    """
    Download steam_app_dict.json from GitHub and save it next to the EXE/script.
    """
    GITHUB_RAW_URL = (
        "https://raw.githubusercontent.com/"
        "KaladinDMP/ARMGDDN-Autocracker-OG-GSE/"
        "main/Resources/AppID/steam_app_dict.json"
    )

    print("Downloading app dictionary from GitHub...")
    try:
        resp = requests.get(GITHUB_RAW_URL, timeout=30)
    except requests.RequestException as e:
        print(f"Error downloading from GitHub: {e}")
        return False

    if resp.status_code != 200:
        print(f"GitHub returned HTTP {resp.status_code}. Using existing local copy.")
        return False

    local_filename = get_file_path("steam_app_dict.json")
    try:
        with open(local_filename, "w", encoding="utf-8") as f:
            f.write(resp.text)
        print("steam_app_dict.json updated from GitHub.")
        return True
    except OSError as e:
        print(f"Error writing local steam_app_dict.json: {e}")
        return False


def is_game(app_id):
    url = f"https://store.steampowered.com/api/appdetails?appids={app_id}"
    try:
        response = requests.get(url, timeout=15)
    except requests.RequestException:
        return False

    if response.status_code == 200:
        try:
            data = json.loads(response.text)
        except json.JSONDecodeError:
            return False

        if str(app_id) in data and data[str(app_id)].get('success'):
            return data[str(app_id)]['data'].get('type') == 'game'
    return False


def search_games(game_name, app_dict, non_game_apps):
    processed_name = preprocess_game_name(game_name)
    matching_games = []

    if not processed_name:
        return matching_games

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
    with open(filename, 'w', encoding="utf-8") as file:
        file.write(str(timestamp))


def load_last_update_timestamp():
    filename = get_file_path("last_update_timestamp.txt")
    if os.path.exists(filename):
        try:
            with open(filename, 'r', encoding="utf-8") as file:
                return float(file.read())
        except (ValueError, OSError):
            return 0
    return 0


# ---------------- main flow ----------------

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
    print("Downloading latest app dictionary from GitHub...")
    if update_app_dict_from_github():
        app_dict = load_app_dict()
        save_last_update_timestamp(current_timestamp)
        print("App dictionary updated successfully from GitHub.")
    else:
        print("Failed to update app dictionary from GitHub. Using existing local copy.")
else:
    print("App dictionary is up to date.")

# Edge case: no app dictionary at all
if not app_dict:
    print()
    print("No app dictionary is available, so I can't search Steam apps.")
    print("Make sure you have an internet connection the first time you run this tool,")
    print("or manually place a valid steam_app_dict.json next to the EXE/script.")
    print("Exiting.")
    sys.exit(1)

# Normal interactive flow
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
            for index, (app_id, gn) in enumerate(updated_matching_games, start=1):
                print(f"{index}. App ID: {app_id}, Game Name: {gn}")

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
                        print("None of these are right. I want to try to search again.")
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
