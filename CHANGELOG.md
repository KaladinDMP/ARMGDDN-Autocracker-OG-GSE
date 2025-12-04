# ARMGDDN Autocracker Changelog

Welcome to the ARMGDDN Autocracker Changelog! Here, we chronicle the thrilling journey of our beloved program as it evolves and grows. Get ready for a wild ride filled with bug fixes, new features, and the occasional twist and turn!

## **v1.2.1 - 12/4/2025**
Quick bugfix release to address a crash reported by the community.

**Highlights**
- 🐛 **Fixed AttributeError Crash:** Resolved a crash in `ARMGDDN.Steam.Settings.exe` that occurred when Steam's CDN reset connections during achievement image downloads.
- 🔧 **Corrected Exception Handling:** `URLError` uses `.reason`, not `.code` (which only exists on `HTTPError`). This was causing crashes when connection resets occurred.

**Acknowledgements**
- Thanks to the [user l95RHl](https://github.com/l95RHl),  who reported this [issue](https://github.com/KaladinDMP/ARMGDDN-Autocracker-OG-GSE/issues/1) on GitHub!

## **v1.2.0 - 11/20/2025**
A big one today — and a huge step toward making ARMGDDN Autocracker truly future-proof.  
The `steam_app_dict.json` no longer depends on Steam’s unstable API — instead, it is now **fully automated via GitHub Actions**, pulled directly into the app once per day, keeping the game list fresh without ever shipping a key or making risky API calls on the user’s machine. Truly hands-off, fully secure, and built to last.

**Highlights**
- 🔁 **Fully Automated App List Updates:** `ARMGDDN.AppID.exe` now updates the massive internal Steam game dictionary once per day directly from GitHub — no API calls and **no user internet keys needed.**
- 🚀 **GitHub Actions Support:** A dedicated GitHub workflow fetches over 200K Steam apps using the store API, cleans them, and commits a fresh `steam_app_dict.json` once per day — all without touching a local PC.
- 🧠 **Zero External Dependencies:** Removed heavy NLTK from the user-side exe, making it lighter, faster, and easier to compile.
- 🔒 **100% Offline Operation:** The program can now fully operate offline using cached data. If a dictionary cannot be downloaded, the app still works normally using the local copy.
- 🧱 **Cleaner & Safer EXE Builds:** `ARMGDDN.AppID.exe` was fully restructured to use relative paths, detect EXE mode, and save all files next to the executable for plug-and-play portability on **any PC.**
- 📁 **Local JSON Storage:** Database files (`steam_appid.txt`, `steam_app_dict.json`, `non_game_apps.json`) are always stored next to the exe—ready for future tools or integrations.

**Acknowledgements**
- Thanks to nothingmore from RIN who caught the 404 from using the old app v2 app list (https://api.steampowered.com/ISteamApps/GetAppList/v2/)
- Major shoutout to GitHub Actions for silently doing 200K+ API calls daily so users don’t have to.

## **v1.1.0 - 5/11/2025** 
It’s here — the  v1.1.0 update! We've been needing this one for a while, and it comes packed with more intelligence, stability, and future-proofing for ARMGDDN.Steam.Settings.exe.  

We’ve tapped into the [SteamLadder](https://steamladder.com/) API to make sure you’re always ahead of the curve when it comes to achievements and DLC recognition — especially for new releases. Plus, we cleaned up some quirks and made sure those pesky 0KB files don't clutter your setup anymore.  

**Highlights**  
- 🔥 **Steam ID Auto-Updater:** ARMGDDN.Steam.Settings.exe now checks the top 20 Steam accounts that own the most games globally via [SteamLadder](https://steamladder.com/) once a week (powered by GitHub Actions in [another repo of mine](https://github.com/KaladinDMP/steam-top-accounts-data)).  
- 📦 **Hardcoded List Expansion:** Top users’ game libraries are scanned and cross-checked. If any Steam IDs are missing from the massive internal list, they’re added automatically.  
- 🧠 **Better DLC/Achievements Support:** This should significantly improve detection for DLC and achievements, especially in newer or frequently updated games.  
- 🧹 **0KB File Prevention:** `dlc.txt` and `stats.txt` will no longer be generated as empty files. If there’s nothing to write, nothing gets created — simple and clean.  

**Notes**  
- Apologies for the delay — we know updates have been a long time coming.  
- Seriously considering finally doing a proper ARMGDDN Autocracker version based on the latest [GBE fork](https://github.com/Detanup01/gbe_fork). If we do, it’ll be a big step forward.

**Acknowledgements**  
- Huge shoutout to the SteamLadder team for their open API.  
- Thanks again to Sak32009, whose earlier fork kicked off this speed-focused era of improvements.

## **v1.0.5 - 10/13/2024**
This update brings a significant speed boost to the steam settings generation process, thanks to a fantastic steam module fork from Sak32009!!

**Highlights**
- Integrated [Sak32009's Steam Module fork](https://github.com/Sak32009/steam_py_fork/tree/fix-cm-servers) to compile the ARMGDDN.Steam.Settings exe.
- This change has GREATLY increased the speed at which a steam settings folder is created.

**Acknowledgements**
- Special thanks to [Sak32009](https://github.com/Sak32009/) for their invaluable contribution!

## **v1.0.4 - 6/25/2024**
Today's update comes with a crucial fix! We tackled a nasty bug that was causing a crash in some games, with 100% Orange Juice being the main culprit. The `steam_settings` folder was left blank, but not anymore! Plus, a quick update on the health front and plans for the future. Let's get into it!

**Highlights**
- Fixed an issue in `ARMGDDN.Steam.Settings.py` (this is the edited Goldberg script generate_emu_config.py) and `achievements_gen.py` that caused crashes on some games.
- Specifically resolved the problem with 100% Orange Juice achievements causing a blank `steam_settings` folder. Now everything should generate correctly!

**Behind the Scenes**
- Been having some health issues lately, but I'm still determined to work on the Goldberg Steam Emu Fork at some point. Thanks for your patience and understanding!


## **v1.0.3 - 6/15/2024**
Today's update is a small one! We've squashed a pesky bug with the context menu icons and made some significant changes to the location of key files. Let's dive in!

**Highlights**
- Fixed an issue with the context menu icon for VD.bat not displaying correctly. Now, your context menu looks as polished as ever!
- Moved `nircmd.exe` to the `Resources/Tools` directory. It's now better organized and easier to find.
- Added `generate_interfaces_file.exe` to the `Resources/Tools` directory. Remember, you need to create the interface file on a legit Steam API DLL before using the autocracker on the DLL.


## **v1.0.2 - 6/12/2024**
A small but mighty update! We've ironed out some kinks from the previous version and made sure everything is running smoother than ever. Get ready for an even better ARMGDDN Autocracker experience! Sorry about the last update....


## **v1.0.1 - 6/11/2024**
Hold onto your hats, folks! v1.0.1 is here, and it's packed with more fixes than a handyman's toolbox!

**Highlights**
- We've given our exe files a fresh coat of paint and updated their version numbers. They're now ready to take on the world!
- ARMGDDN.Main, ARMGDDN.Cold.Client, and ARMGDDN.Autocracker have undergone some serious therapy to resolve their appid issues. No more falling back on old habits!
- Steam_appid.txts with old app id's have been shown the door. Out with the old, in with the new!
- We've tidied up the clears and pauses to make the flow as smooth as a baby's bottom. Readability is key, folks!
- Installing and removing context menu reg edits now come with a friendly warning about the talking. Adjust your volume accordingly, unless you enjoy surprises!
- Steamclient files in the Api folder have been given their marching orders. They weren't pulling their weight anyway.
- We've embraced the power of three and switched to the more common 3-number version code (X.X.X). Who needs that extra X anyway?

**Behind the Scenes**
- RAW files have been updated, and a shiny new dev branch has been created. It's like a secret hideout for all the cool stuff that didn't make it into the release version.
- We're dreaming big with plans for a database of games and non-games. Imagine a world where everyone contributes to a shared knowledge base, making the app faster and smarter! Also planning on a fork for [GSE fork](https://github.com/otavepto/gbe_fork) compatibility

**Shout-outs**
A huge thank you to Cybah for their meticulous review and unwavering dedication to finding every last bit of funkiness in the app. You're the real MVP!

While we couldn't reproduce the cold client issue mentioned [here](https://cs.rin.ru/forum/viewtopic.php?p=3069355#p3069355), we've got our eyes peeled. If it rears its ugly head again, we'll be ready to pounce!

Stay tuned for more exciting updates as we continue to explore the [GSE fork](https://github.com/otavepto/gbe_fork). It's going to be a wild ride!

## **v1.0.0.0 - 6/9/2024**
The day it all began! v1.0.0.0 burst onto the scene, marking the birth of ARMGDDN Autocracker. It was a humble beginning, but little did we know, it was the start of something extraordinary!

**Features**
- Everything! It's the initial release, after all. 😄

So, there you have it, folks! The ARMGDDN Autocracker Changelog, where we chronicle the ups, the downs, and the occasional sideways maneuvers of our beloved program. Stay tuned for more thrilling updates as we continue to shape the future of ARMGDDN Autocracker!

