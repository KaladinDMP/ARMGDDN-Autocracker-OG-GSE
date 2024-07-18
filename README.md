# ARMGDDN Autocracker 🎮🔧

![ARMGDDN Autocracker Logo](https://github.com/KaladinDMP/ARMGDDN-Autocracker/assets/92135051/ebcf7a21-8e5d-44e2-9165-cb280d8d275c)
[cs.rin.ru introduction page](https://cs.rin.ru/forum/viewtopic.php?f=20&t=141375)

ARMGDDN Autocracker is a cutting-edge tool designed to revolutionize the way you crack and prepare Steam games for an unparalleled gaming experience. With its user-friendly interface and powerful features, ARMGDDN Autocracker empowers gamers and enthusiasts to effortlessly unlock the full potential of their favorite games. 

**WARNING:** This is not a tool for amateurs but rather a tool to make the methods easier for those with a general knowledge of these techniques. You will still need to find the EXE that needs its Steam stub removed, the Steam API DLL that needs cracking, and know when and where a Cold Client Loader or a VD bat is needed or a steam interfaces file needs to be created.

## ✨ Features

### 🖱️ Context Menu Integration
ARMGDDN Autocracker seamlessly integrates with your Windows Explorer, offering convenient context menu commands for both EXE and DLL files.

**EXE Files:**
 - **ARMGDDN Autocracker:** A menu for all the EXE features in case you want to use more than one option.
 - **ARMGDDN Cold Client:** Prepare your Steam game for use with the Cold Client Loader.
 - **ARMGDDN Steam Stub Remover:** Effortlessly check for and remove Steam stubs from your game EXEs.
 - **ARMGDDN VD Batmaker:** Generate VD bat files optimized for Virtual Desktop owners (VR ONLY).
   
**DLL Files:**
 - **ARMGDDN Autocracker:** Automatically replace the original DLL file (steam_api64.dll or steam_api.dll) with the experimental generic Goldberg Steam emulator.
 - **ARMGDDN Steam Interfaces Maker:** Generate Steam interfaces for the original Steam API DLL files (not the Goldberg one).

### 🖱️ Drag and Drop Support
In addition to the optional context menu options, ARMGDDN Autocracker supports intuitive drag and drop functionality. Simply drag and drop your EXE or DLL file onto the main executable to initiate the cracking process.  You can only do EXE fixes to EXEs, and DLL fixes on the steam_api DLLs (meaning you can't do both from one drag and drop or one right click context menu).

### 🔍 Steam App ID Detection
ARMGDDN Autocracker intelligently searches for the steam_appid.txt file in the directory of the dropped file. If found, it automatically copies the file to the appropriate location. If the steam_appid.txt file is not detected, ARMGDDN Autocracker prompts you to enter the game name using the ARMGDDN.App.ID utility. In case the app ID is still not found, you have the flexibility to enter it manually.

### 🔓 Comprehensive Cracking
With ARMGDDN Autocracker's gentle nudging, you can effortlessly crack any game with basic Steam DRM. Say goodbye to the need for additional tools or complex procedures and enjoy a seamless gaming experience.

## 📖 Usage

1. Extract ARMGDDN Autocracker to its new "forever home".

2. To use the context menu commands:
  - Install the context menu options by running ContextMenuRegEdits.exe from the parent directory as an administrator. There's a fast way to safely remove them as well.
  - Alternatively, you can use the drag and drop functionality to avoid modifying the registry.
  - Right-click on an EXE file and select the desired option from the ARMGDDN Autocracker context submenu.
  - Right-click on a steam_api64.dll or steam_api.dll and select the "Steam Interfaces" or "ARMGDDN Autocracker" option.
  - Follow the on-screen prompts to complete the cracking process.

3. To use the drag and drop functionality:
  - Drag and drop an EXE or DLL file onto the ARMGDDN Main executable.
  - Follow the on-screen prompts to complete the cracking process.

4. If the steam_appid.txt file is not automatically detected, ARMGDDN Autocracker will prompt you to enter the game name using the ARMGDDN.App.ID utility. As a fallback, you can enter it manually.

5. Enjoy your cracked games and embark on thrilling adventures!

## 🛠️ Requirements

- Windows operating system
- NET Framework 4.5 or higher
- Basic knowledge of current cracking methods
- A bit of common sense
## ⚠️ Disclaimer

Please note that cracking and modifying game files may violate the terms of service of the game or the platform it is associated with. Use ARMGDDN Autocracker at your own risk and ensure that you have the necessary permissions and rights to modify the game files. This disclaimer serves as a reminder to use the tool responsibly and in compliance with applicable laws and regulations.

## 🙏 Acknowledgements

ARMGDDN Autocracker is made possible by the following components and tools:

- Goldberg Experimental Steam Emulator by Mr. Goldberg
- Goldberg Experimental Steamclient Loader by Mr. Goldberg (which is largely based on a  [ColdClient Loader by Rat431 called ColdAPI_Steam](https://www.github.com/Rat431/ColdAPI_Steam/releases/latest))
- Goldberg Steam Interfaces Generator
- A highly edited Goldberg Python script to generate emulator configuration
- Steamless by Atom0s
- AppDetails and ISteamApps AppList Steam APIs

ARMGDDN Autocracker is proudly developed by DeliciousMeatPop and George Jefferson, the owners of ARMGDDN Games. George Jefferson wrote the App ID Python script and provided moral support and invaluable insight into testing the program, while DeliciousMeatPop made the heavy mistakes.

## 💡 Where to get the required components
To set up your own ARMGDDN Autocracker, you'll need the Goldberg Steam Emulator, the Goldberg Cold Client Loader, a highly edited Goldberg Python Steam App ID fetching script, and the Steamless program. Here are the locations where you can find these components without our edits:

- Goldberg Experimental Steam Emulator: [https://gitlab.com/Mr_Goldberg/goldberg_emulator](https://gitlab.com/Mr_Goldberg/goldberg_emulator)
- Goldberg Experimental Steamclient Loader: [https://gitlab.com/Mr_Goldberg/goldberg_emulator](https://gitlab.com/Mr_Goldberg/goldberg_emulator)
- The unedited Goldberg Python script: [https://gitlab.com/Mr_Goldberg/goldberg_emulator/-/tree/master/scripts](https://gitlab.com/Mr_Goldberg/goldberg_emulator/-/tree/master/scripts)
- Goldberg Steam Interfaces Generator [https://gitlab.com/Mr_Goldberg/goldberg_emulator](https://gitlab.com/Mr_Goldberg/goldberg_emulator)
- Steamless: [https://github.com/atom0s/Steamless](https://github.com/atom0s/Steamless)

## 🌟 Support

If you encounter any issues, have questions, or want to connect with fellow gamers, join our vibrant support channel at [https://t.me/ARMGDDNGames](https://t.me/ARMGDNGames). Alternatively, you can reach out to our dedicated support team, leave an issue here or on our [cs.rin.ru introduction page](https://cs.rin.ru/forum/viewtopic.php?f=20&t=141375)

---

Thank you for choosing ARMGDDN Autocracker. May your gaming adventures be filled with excitement and endless possibilities! 🚀🎉
