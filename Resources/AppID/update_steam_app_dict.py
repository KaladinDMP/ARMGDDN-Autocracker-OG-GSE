import os
import sys
import json
import time
import requests

try:
    import nltk
    from nltk.tokenize import word_tokenize
    from nltk.corpus import stopwords
    nltk_available = True
except ImportError:
    nltk_available = False

if nltk_available:
    nltk.download('punkt')
    nltk.download('stopwords')


def preprocess_game_name(game_name: str) -> str:
    if not isinstance(game_name, str):
        return ""

    game_name = ''.join(ch for ch in game_name if ch.isalnum() or ch.isspace())

    if not nltk_available:
        return game_name.lower().strip()

    tokens = word_tokenize(game_name)
    stop_words = set(stopwords.words('english'))
    filtered = [w.lower() for w in tokens if w.isalnum() and w.lower() not in stop_words]
    return " ".join(filtered)


def fetch_all_apps(steam_api_key: str):
    base_url = "https://api.steampowered.com/IStoreService/GetAppList/v1"
    all_apps = []
    last_appid = 0
    max_results = 50000
    page = 1

    while True:
        params = {
            "key": steam_api_key,
            "include_games": 1,
            "include_dlc": 1,
            "include_software": 1,
            "include_videos": 1,
            "include_hardware": 1,
            "last_appid": last_appid,
            "max_results": max_results,
        }
        print(f"Requesting page {page} with last_appid={last_appid}...")
        resp = requests.get(base_url, params=params, timeout=60)
        if resp.status_code != 200:
            print(f"HTTP {resp.status_code} from IStoreService/GetAppList. Body:")
            print(resp.text[:500])
            break

        data = resp.json()
        apps = data.get("response", {}).get("apps", [])
        if not apps:
            print("No more apps returned, done.")
            break

        all_apps.extend(apps)
        print(f"Got {len(apps)} apps in this page, total so far {len(all_apps)}")

        if len(apps) < max_results:
            print("Final page reached.")
            break

        last_appid = apps[-1].get("appid", last_appid)
        page += 1
        time.sleep(1)

    print(f"Total apps fetched: {len(all_apps)}")
    return all_apps


def build_app_dict(apps):
    app_dict = {}
    total = len(apps)
    for i, app in enumerate(apps, start=1):
        appid = app.get("appid")
        name = app.get("name")
        if not appid or not name:
            continue
        appid_str = str(appid)
        processed = preprocess_game_name(name)
        app_dict[appid_str] = {
            "original_name": name,
            "processed_name": processed
        }
        if i % 20000 == 0:
            print(f"Processed {i}/{total} apps...")

    print(f"Finished building app_dict with {len(app_dict)} entries.")
    return app_dict


def main():
    steam_api_key = os.environ.get("STEAM_API_KEY")
    if not steam_api_key:
        print("STEAM_API_KEY env var is not set.")
        sys.exit(1)

    apps = fetch_all_apps(steam_api_key)
    if not apps:
        print("No apps fetched, aborting.")
        sys.exit(1)

    app_dict = build_app_dict(apps)

    out_file = "steam_app_dict.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(app_dict, f)

    print(f"Wrote {len(app_dict)} entries to {out_file}")


if __name__ == "__main__":
    main()
