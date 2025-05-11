USERNAME = "AchievementTestAccount"
PASSWORD = "Nogamesonthisaccountdontbother."

import os
import sys
import json
import urllib.request
import urllib.error
import threading
import queue

HARDCODED_STEAM_IDS = [
    76561198017975643,
    76561198028121353,
    76561197979911851,
    76561198355953202,
    76561198217186687,
    76561197993544755,
    76561198001237877,
    76561198237402290,
    76561198152618007,
    76561198213148949,
    76561198037867621,
    76561197969050296,
    76561198134044398,
    76561198001678750,
    76561198094227663,
    76561197973009892,
    76561198019712127,
    76561197976597747,
    76561197963550511,
    76561198044596404,
    76561198119667710,
    76561197962473290,
    76561197969810632,
    76561198095049646,
    76561197995070100,
    76561198085065107,
    76561197996432822,
    76561199492215670,
    76561198313790296,
    76561198033715344,
    76561198256917957,
    76561198063574735,
    76561198388522904,
    76561197970825215,
    76561198027214426,
    76561198035900006,
    76561198154462478,
    76561198281128349,
    76561198367471798,
    76561198407953371,
    76561199130977924,
    76561197976968076,
    76561198235911884,
    76561198104323854,
    76561198062901118,
    76561198842864763,
    76561198077213101,
    76561198027233260,
    76561198122859224,
    76561198063728345,
    76561198010615256,
    76561198008181611,
    76561198001221571,
    76561197974742349,
    76561198082995144,
    76561197968410781,
    76561198890581618,
    76561197976796589,
    76561197971011821,
    76561198097945516,
    76561198118726910,
    76561197993312863,
    76561198326510209,
    76561197979667190,
    76561197990233857,
    76561197978640923,
    76561198121398682,
    76561198158932704,
    76561198109083829,
    76561197963534359,
    76561198019009765,
    76561197981111953,
    76561198077248235,
    76561198139084236,
    76561198093753361,
    76561198382166453,
    76561198096081579,
    76561198124872187,
    76561198045455280,
    76561197992133229,
    76561198152760885,
    76561198048373585,
    76561198172367910,
    76561198037809069,
    76561198005337430,
    76561198396723427,
    76561197994616562,
    76561198026221141,
    76561199168919006,
    76561198318944318,
    76561199353305847,
    76561197983517848,
    76561198102767019,
    76561199080934614,
    76561197972951657,
    76561198006391846,
    76561198155124847,
    76561198040421250,
    76561198318111105,
    76561198021180815,
    76561198044387084,
    76561197984010356,
    76561198251835488,
    76561197992548975,
    76561198017902347,
    76561198008797636,
    76561198025858988,
    76561198061393233,
    76561198128158703,
    76561198015685843,
    76561198192399786,
    76561197965978376,
    76561197972378106,
    76561198015856631,
    76561198417144062,
    76561197988664525,
    76561198219343843,
    76561198031837797,
    76561198039492467,
    76561198315929726,
    76561197971026489,
    76561197982718230,
    76561198105279930,
    76561198047438206,
    76561198054210948,
    76561198264362271,
    76561198028011423,
    76561198020125851,
    76561197973230221,
    76561197995008105,
    76561198050474710,
    76561198252374474,
    76561198996604130,
    76561199173688191,
    76561197984235967,
    76561197968401807,
    76561198106206019,
    76561198842603734,
    76561198034213886,
    76561197997477460,
    76561198015992850,
    76561198045540632,
    76561199187733000,
    76561198025653291,
    76561197969148931,
    76561197975329196,
    76561198043532513,
    76561198029503957,
    76561198096632451,
    76561198051887711,
    76561198018254158,
    76561197970246998,
    76561198111433283,
    76561198057648189,
    76561198029532782,
    76561198009596142,
    76561198004332929,
    76561198031164839,
    76561198027668357,
    76561198294806446,
    76561198025391492,
    76561198048151962,
    76561197986240493,
    76561198003041763,
    76561198072361453,
    76561198020746864,
    76561198042965266,
    76561198269242105,
    76561198104561325,
    76561198046642155,
    76561198172925593,
    76561198072936438,
    76561198086250077,
    76561198141387426,
    76561198426000196,
    76561198154522279,
    76561198006715789,
    76561198106145311,
    76561198027066612,
    76561197992105918,
    76561197962630138,
    76561197985091630,
    76561198171791210,
    76561198120120943,
    76561198071709714,
    76561198844130640,
    76561198283395702,
    76561198042781427,
    76561198124865933,
    76561198051725954,
    76561198443388781,
    76561197994575642,
    76561197981228012,
    76561198032614383,
    76561198015514779,
    76561198088628817,
    76561198074920693,
    76561197991699268,
    76561198079227501,
    76561197981027062,
    76561198122276418,
    76561198019841907,
    76561197972259379,
    76561198070220549,
    76561198085238363,
    76561198090111762,
    76561197991613008,
    76561197970545939,
    76561198060520130,
    76561198093579202,
    76561198079896896,
    76561198846208086,
    76561197973701057,
    76561198026306582,
    76561197988052802,
    76561197977920776,
    76561198150467988,
    76561198427572372,
    76561198034906703,
    76561198028428529,
    76561198098314980,
    76561198117483409,
    76561198007200913,
    76561197966617426,
    76561198008549198,
    76561197982273259,
    76561198165450871,
    76561198002535276,
    76561198025111129,
    76561198101049562,
    76561197969365800,
    76561197984605215,
    76561198413266831,
    76561198413088851,
    76561198004532679,
    76561197970307937,
    76561198811114019,
    76561197970360549,
    76561197972529138,
    76561198119915053,
    76561197970970678,
    76561198356842617,
    76561198083977059,
    76561198027917594,
    76561197967716198,
    76561198831075066,
    76561198033967307,
    76561198028125071,
    76561198217979953,
]

STEAM_IDS_URL = "https://raw.githubusercontent.com/KaladinDMP/steam-top-accounts-data/main/steam_ids_only.txt"
LOCAL_STEAM_IDS_FILE = "steam_ids_cache.txt"

def get_base_path():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    else:
        return os.path.dirname(os.path.abspath(__file__))

BASE_PATH = get_base_path()
LOCAL_STEAM_IDS_FILE = os.path.join(BASE_PATH, LOCAL_STEAM_IDS_FILE)

def download_and_merge_steam_ids():
    """
    1. Start with hardcoded list
    2. Download GitHub list
    3. Add any NEW IDs from GitHub to hardcoded list
    4. Return combined list
    """
    print(f"Starting with {len(HARDCODED_STEAM_IDS)} hardcoded Steam IDs...")
    
    final_steam_ids = HARDCODED_STEAM_IDS.copy()
    
    try:
        print("Attempting to download Steam IDs from GitHub...")
        with urllib.request.urlopen(STEAM_IDS_URL) as response:
            content = response.read().decode('utf-8')
            
            with open(LOCAL_STEAM_IDS_FILE, 'w') as f:
                f.write(content)
            print(f"Successfully saved Steam IDs to local cache: {LOCAL_STEAM_IDS_FILE}")
            
            github_steam_ids = []
            for line in content.strip().split('\n'):
                line = line.strip()
                if line:  
                    try:
                        github_steam_ids.append(int(line))
                    except ValueError:
                        print(f"Warning: Could not convert '{line}' to Steam ID")
            
            print(f"Downloaded {len(github_steam_ids)} Steam IDs from GitHub")
            
            new_ids = 0
            for steam_id in github_steam_ids:
                if steam_id not in HARDCODED_STEAM_IDS:
                    final_steam_ids.append(steam_id)
                    new_ids += 1
                    print(f"Adding new Steam ID: {steam_id}")
            
            print(f"Added {new_ids} new Steam IDs from GitHub")
            print(f"Final list contains {len(final_steam_ids)} Steam IDs")
            
    except Exception as e:
        print(f"Error downloading Steam IDs from GitHub: {e}")
        print("Using hardcoded list only...")
        
        try:
            with open(LOCAL_STEAM_IDS_FILE, 'r') as f:
                content = f.read()
                github_steam_ids = []
                for line in content.strip().split('\n'):
                    line = line.strip()
                    if line:
                        try:
                            github_steam_ids.append(int(line))
                        except ValueError:
                            print(f"Warning: Could not convert '{line}' to Steam ID")
                
                print(f"Loaded {len(github_steam_ids)} Steam IDs from local cache")
                
                new_ids = 0
                for steam_id in github_steam_ids:
                    if steam_id not in HARDCODED_STEAM_IDS:
                        final_steam_ids.append(steam_id)
                        new_ids += 1
                        print(f"Adding new Steam ID from cache: {steam_id}")
                
                print(f"Added {new_ids} new Steam IDs from cache")
                print(f"Final list contains {len(final_steam_ids)} Steam IDs")
                
        except Exception as cache_error:
            print(f"Error loading from local cache: {cache_error}")
            print("No local cache available. Using hardcoded list only.")
    
    return final_steam_ids

TOP_OWNER_IDS = download_and_merge_steam_ids()

from stats_schema_achievement_gen import achievements_gen
from controller_config_generator import parse_controller_vdf
from steam.client import SteamClient
from steam.client.cdn import CDNClient
from steam.enums import common
from steam.enums.common import EResult
from steam.enums.emsg import EMsg
from steam.core.msg import MsgProto
import steam.protobufs.steammessages_publishedfile_pb2

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
    print("\nUsage: ARMGDDN.Steam.Settings.exe APPID \n\nExample:ARMGDDN.Steam.Settings.exe 480\n".format(sys.argv[0], sys.argv[0]))
    sys.exit(1)

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
            sys.exit(1)

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
    
    if not TOP_OWNER_IDS:
        print("Warning: No Steam IDs available. Skipping achievement stats generation.")
        return
    
    stats_generated = False 
    
    steam_id_list = TOP_OWNER_IDS + [client.steam_id]
    for x in steam_id_list:
        out = get_stats_schema(client, game_id, x)
        if out is not None:
            if len(out.body.schema) > 0:
                try:
                    achievements, stats = achievements_gen.generate_stats_achievements(out.body.schema, output_directory)
                    
                    if stats and len(stats) > 0:
                        stats_generated = True
                        
                        stats_output = ""
                        for s in stats:
                            default_num = 0
                            if s['type'] == 'int':
                                try:
                                    default_num = int(s['default'])
                                except ValueError:
                                    try:
                                        default_num = int(float(s['default']))
                                    except ValueError:
                                        default_num = 0
                            else:
                                try:
                                    default_num = float(s['default'])
                                except ValueError:
                                    default_num = 0.0
                            stats_output += "{}={}={}\n".format(s['name'], s['type'], default_num)
                        
                        if stats_output.strip():
                            with open(os.path.join(output_directory, "stats.txt"), 'w', encoding='utf-8') as f:
                                f.write(stats_output)
                            print(f"Created stats.txt with {len(stats)} stats")
                    
                    for ach in achievements:
                        if "icon" in ach:
                            images_to_download.append(ach["icon"])
                        if "icon_gray" in ach:
                            images_to_download.append(ach["icon_gray"])
                    break
                except ValueError as e:
                    print(f"Error generating stats achievements for Steam ID {x}: {e}")
                    continue
            else:
                pass

    if len(images_to_download) > 0:
        if not os.path.exists(achievement_images_dir):
            os.makedirs(achievement_images_dir)
        download_achievement_images(game_id, images_to_download, achievement_images_dir)
    
    return stats_generated

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
        try:
            generate_achievement_stats(client, appid, out_dir)
        except Exception as e:
            print(f"Unhandled exception during achievement stats generation for appid {appid}: {e}")

    with open(os.path.join(out_dir, "steam_appid.txt"), 'w') as f:
        f.write(str(appid))

    dlc_config_list = []
    dlc_list, depot_app_list = get_dlc(game_info)
    dlc_infos_backup = ""
    if len(dlc_list) > 0:
        dlc_raw = client.get_product_info(apps=dlc_list)["apps"]
        for dlc in dlc_raw:
            try:
                dlc_config_list.append((dlc, dlc_raw[dlc]["common"]["name"]))
            except:
                dlc_config_list.append((dlc, None))
        dlc_infos_backup = json.dumps(dlc_raw, indent=4)

    if dlc_config_list:
        with open(os.path.join(out_dir, "DLC.txt"), 'w', encoding="utf-8") as f:
            for x in dlc_config_list:
                if (x[1] is not None):
                    f.write("{}={}\n".format(x[0], x[1]))
        print(f"DLC.txt created with {len(dlc_config_list)} entries")
    else:
        print("No DLC found, skipping DLC.txt creation")