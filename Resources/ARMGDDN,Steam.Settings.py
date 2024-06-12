USERNAME = "AchievementTestAccount"
PASSWORD = "Nogamesonthisaccountdontbother."

#steam ids with public profiles that own a lot of games
TOP_OWNER_IDS = [76561198028121353, 76561198001237877, 76561198355625888, 76561198001678750, 76561198237402290, 76561197979911851, 76561198152618007, 76561197969050296, 76561198213148949, 76561198037867621, 76561198108581917]

from stats_schema_achievement_gen import achievements_gen
from controller_config_generator import parse_controller_vdf
from steam.client import SteamClient
from steam.client.cdn import CDNClient
from steam.enums import common
from steam.enums.common import EResult
from steam.enums.emsg import EMsg
from steam.core.msg import MsgProto
import steam.protobufs.steammessages_publishedfile_pb2
import os
import sys
import json
import urllib.request
import urllib.error
import threading
import queue

def setup_protobuf_path():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    protobuf_dir = os.path.join(current_dir, 'new_venv', 'Lib', 'site-packages', 'steam', 'protobufs')
    
    if protobuf_dir not in sys.path:
        sys.path.append(protobuf_dir)

setup_protobuf_path()

try:
    from steam.protobufs import steammessages_inventory_pb2
except ImportError as e:
    print(f"Error importing protobuf module: {e}")
    
prompt_for_unavailable = True

if len(sys.argv) < 2:
    print("\nUsage: {} appid appid appid etc..\n\nExample: {} 480\n".format(sys.argv[0], sys.argv[0]))
    exit(1)

appids = []
for id in sys.argv[1:]:
    appids +=  [int(id)]

client = SteamClient()

if (len(USERNAME) == 0 or len(PASSWORD) == 0):
    client.cli_login()
else:
    result = client.login(USERNAME, password=PASSWORD)
    auth_code, two_factor_code = None, None
    while result in (EResult.AccountLogonDenied, EResult.InvalidLoginAuthCode,
                        EResult.AccountLoginDeniedNeedTwoFactor, EResult.TwoFactorCodeMismatch,
                        EResult.TryAnotherCM, EResult.ServiceUnavailable,
                        EResult.InvalidPassword,
                        ):

        if result == EResult.InvalidPassword:
            print("invalid password, the password you set is wrong.")
            exit(1)

        elif result in (EResult.AccountLogonDenied, EResult.InvalidLoginAuthCode):
            prompt = ("Enter email code: " if result == EResult.AccountLogonDenied else
                        "Incorrect code. Enter email code: ")
            auth_code, two_factor_code = input(prompt), None

        elif result in (EResult.AccountLoginDeniedNeedTwoFactor, EResult.TwoFactorCodeMismatch):
            prompt = ("Enter 2FA code: " if result == EResult.AccountLoginDeniedNeedTwoFactor else
                        "Incorrect code. Enter 2FA code: ")
            auth_code, two_factor_code = None, input(prompt)

        elif result in (EResult.TryAnotherCM, EResult.ServiceUnavailable):
            if prompt_for_unavailable and result == EResult.ServiceUnavailable:
                while True:
                    answer = input("Steam is down. Keep retrying? [y/n]: ").lower()
                    if answer in 'yn': break

                prompt_for_unavailable = False
                if answer == 'n': break

            client.reconnect(maxdelay=15)

        result = client.login(USERNAME, PASSWORD, None, auth_code, two_factor_code)


def get_stats_schema(client, game_id, owner_id):
    message = MsgProto(EMsg.ClientGetUserStats)
    message.body.game_id = game_id
    message.body.schema_local_version = -1
    message.body.crc_stats = 0
    message.body.steam_id_for_user = owner_id

    client.send(message)
    return client.wait_msg(EMsg.ClientGetUserStatsResponse, timeout=5)

def download_achievement_images(game_id, image_names, output_folder):
    q = queue.Queue()

    def downloader_thread():
        while True:
            name = q.get()
            succeeded = False
            if name is None:
                q.task_done()
                return
            for u in ["https://cdn.akamai.steamstatic.com/steamcommunity/public/images/apps/", "https://cdn.cloudflare.steamstatic.com/steamcommunity/public/images/apps/"]:
                url = "{}{}/{}".format(u, game_id, name)
                try:
                    with urllib.request.urlopen(url) as response:
                        image_data = response.read()
                        with open(os.path.join(output_folder, name), "wb") as f:
                            f.write(image_data)
                        succeeded = True
                        break
                except urllib.error.HTTPError as e:
                    print("HTTPError downloading", url, e.code)
                except urllib.error.URLError as e:
                    print("URLError downloading", url, e.code)
            if not succeeded:
                print("error could not download", name)
            q.task_done()

    num_threads = 20
    for i in range(num_threads):
        threading.Thread(target=downloader_thread, daemon=True).start()

    for name in image_names:
        q.put(name)
    q.join()

    for i in range(num_threads):
        q.put(None)
    q.join()


def generate_achievement_stats(client, game_id, output_directory):
    achievement_images_dir = os.path.join(output_directory, "achievement_images")
    images_to_download = []
    steam_id_list = TOP_OWNER_IDS + [client.steam_id]
    for x in steam_id_list:
        out = get_stats_schema(client, game_id, x)
        if out is not None:
            if len(out.body.schema) > 0:
                achievements, stats = achievements_gen.generate_stats_achievements(out.body.schema, output_directory)
                for ach in achievements:
                    if "icon" in ach:
                        images_to_download.append(ach["icon"])
                    if "icon_gray" in ach:
                        images_to_download.append(ach["icon_gray"])
                break
            else:
                pass

    if (len(images_to_download) > 0):
        if not os.path.exists(achievement_images_dir):
            os.makedirs(achievement_images_dir)
        download_achievement_images(game_id, images_to_download, achievement_images_dir)

def get_ugc_info(client, published_file_id):
    return client.send_um_and_wait('PublishedFile.GetDetails#1', {
            'publishedfileids': [published_file_id],
            'includetags': False,
            'includeadditionalpreviews': False,
            'includechildren': False,
            'includekvtags': False,
            'includevotes': False,
            'short_description': True,
            'includeforsaledata': False,
            'includemetadata': False,
            'language': 0
        })

def download_published_file(client, published_file_id, output_directory):
    ugc_info = get_ugc_info(client, published_file_id)

    if (ugc_info is None):
        print("failed getting published file", published_file_id)
        return None

    file_details = ugc_info.body.publishedfiledetails[0]
    if (file_details.result != EResult.OK):
        print("failed getting published file", published_file_id, file_details.result)
        return None

    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    with open(os.path.join(output_directory, "info.txt"), "w") as f:
        f.write(str(ugc_info.body))

    if len(file_details.file_url) > 0:
        with urllib.request.urlopen(file_details.file_url) as response:
            data = response.read()
            with open(os.path.join(output_directory, file_details.filename.replace("/", "_").replace("\\", "_")), "wb") as f:
                f.write(data)
            return data
        return None
    else:
        print("Could not download file", published_file_id, "no url (you can ignore this if the game doesn't need a controller config)")
        return None


def get_inventory_info(client, game_id):
    return client.send_um_and_wait('Inventory.GetItemDefMeta#1', {
            'appid': game_id
        })

def generate_inventory(client, game_id):
    inventory = get_inventory_info(client, appid)
    if inventory.header.eresult != EResult.OK:
        return None

    url = "https://api.steampowered.com/IGameInventory/GetItemDefArchive/v0001?appid={}&digest={}".format(game_id, inventory.body.digest)
    try:
        with urllib.request.urlopen(url) as response:
            return response.read()
    except urllib.error.HTTPError as e:
        print("HTTPError getting", url, e.code)
    except urllib.error.URLError as e:
        print("URLError getting", url, e.code)
    return None

def get_dlc(raw_infos):
    try:
        try:
            dlc_list = set(map(lambda a: int(a), raw_infos["extended"]["listofdlc"].split(",")))
        except:
            dlc_list = set()
        depot_app_list = set()
        if "depots" in raw_infos:
            depots = raw_infos["depots"]
            for dep in depots:
                depot_info = depots[dep]
                if "dlcappid" in depot_info:
                    dlc_list.add(int(depot_info["dlcappid"]))
                if "depotfromapp" in depot_info:
                    depot_app_list.add(int(depot_info["depotfromapp"]))
        return (dlc_list, depot_app_list)
    except:
        print("could not get dlc infos, are there any dlcs ?")
        return (set(), set())

for appid in appids:
    out_dir = "steam_settings"

    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    print("outputting config to", out_dir)

    raw = client.get_product_info(apps=[appid])
    game_info = raw["apps"][appid]

    if "common" in game_info:
        game_info_common = game_info["common"]
        generate_achievement_stats(client, appid, out_dir)

    with open(os.path.join(out_dir, "steam_appid.txt"), 'w') as f:
        f.write(str(appid))

    dlc_config_list = []
    dlc_list, depot_app_list = get_dlc(game_info)
    dlc_infos_backup = ""
    if (len(dlc_list) > 0):
        dlc_raw = client.get_product_info(apps=dlc_list)["apps"]
        for dlc in dlc_raw:
            try:
                dlc_config_list.append((dlc, dlc_raw[dlc]["common"]["name"]))
            except:
                dlc_config_list.append((dlc, None))
        dlc_infos_backup = json.dumps(dlc_raw, indent=4)

    with open(os.path.join(out_dir, "DLC.txt"), 'w', encoding="utf-8") as f:
        for x in dlc_config_list:
            if (x[1] is not None):
                f.write("{}={}\n".format(x[0], x[1]))