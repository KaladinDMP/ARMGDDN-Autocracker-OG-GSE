@echo off
setlocal
set "scriptDir=%~dp0"
set "nircmdPath=%scriptDir%Resources\Tools\nircmd.exe"
if not exist "%nircmdPath%" (
    echo nircmd.exe not found in the Resources directory.
    echo Please ensure nircmd.exe is in the Resources directory.
    pause
    exit /b
)
"%nircmdPath%" infobox "This Script TALKS." "Warning !"
"%nircmdPath%" infobox "LOUDLY..." "Warning !" 
"%nircmdPath%" infobox "Turn down your volume NOW to avoid soiling your undies..." "Warning !" 
"%nircmdPath%" infobox "Ill wait..." "Warning !" 
CLS
"%nircmdPath%" speak text "This script needs admin to run."
net session >nul 2>&1
if %errorLevel% == 0 (
    echo Running with administrative privileges.
) else (
    echo This script requires administrative privileges to modify the registry.
    echo Please run this script as an administrator.
    pause
    exit /b
)
"%nircmdPath%" speak text "Welcome, Enjoy using Armageddon Auto Cracker. Holler back young one. Woot Woot"
"%nircmdPath%" trayballoon "ARMGDDN Autocracker" "Welcome to ARMGDDN Autocracker! This will add context menu options for executable and .dll files." "D:\Downloads\goldberg\ARMGDDNAutocracker\Resources\ARMGDDN.Autocracker.exe" 5000
set "iconPath=%scriptDir%Resources\ARMGDDN.Autocracker.exe,0"
set "steamStubIconPath=%scriptDir%Resources\SteamlessCLI\Steamless.CLI.exe,0"
set "coldClientIconPath=%scriptDir%Resources\ARMGDDN.Cold.Client.exe,0"
set "vdbatIconPath=%scriptDir%Resources\ARMGDDN.VD.Batmaker.exe,0"
set "mainBatPath=%scriptDir%ARMGDDN.Main.exe"
set "SIToolsPath=%scriptDir%Resources\Tools\generate_interfaces_file.exe"
echo Adding registry entries...
"%nircmdPath%" speak text "Adding registry entries to make this easier."
reg add "HKEY_CLASSES_ROOT\dllfile\shell\AutoCracker" /v "Icon" /t REG_SZ /d "%iconPath%" /f
reg add "HKEY_CLASSES_ROOT\dllfile\shell\AutoCracker" /ve /t REG_SZ /d "ARMGDDN Autocracker" /f
reg add "HKEY_CLASSES_ROOT\dllfile\shell\AutoCracker\command" /ve /t REG_SZ /d "\"%mainBatPath%\" \"%%1\"" /f
"%nircmdPath%" speak text "Added the autocracker context menu for steam API dll files"
reg add "HKEY_CLASSES_ROOT\dllfile\shell\SteamInterfaces" /v "Icon" /t REG_SZ /d "%coldClientIconPath%" /f
reg add "HKEY_CLASSES_ROOT\dllfile\shell\SteamInterfaces" /ve /t REG_SZ /d "Steam Interfaces" /f
reg add "HKEY_CLASSES_ROOT\dllfile\shell\SteamInterfaces\command" /ve /t REG_SZ /d "\"%SIToolsPath%\" \"%%1\"" /f
"%nircmdPath%" speak text "Added the autocracker context menu for creating steam interface text files"
reg add "HKEY_CLASSES_ROOT\exefile\shell\AutoCracker" /v "Icon" /t REG_SZ /d "%iconPath%" /f
reg add "HKEY_CLASSES_ROOT\exefile\shell\AutoCracker" /ve /t REG_SZ /d "ARMGDDN Autocracker" /f
reg add "HKEY_CLASSES_ROOT\exefile\shell\AutoCracker\command" /ve /t REG_SZ /d "\"%mainBatPath%\" \"%%1\"" /f
"%nircmdPath%" speak text "Added the autocracker context menu for executable files"
reg add "HKEY_CLASSES_ROOT\exefile\shell\ColdClient" /v "Icon" /t REG_SZ /d "%coldClientIconPath%" /f
reg add "HKEY_CLASSES_ROOT\exefile\shell\ColdClient" /ve /t REG_SZ /d "ARMGDDN Cold Client" /f
reg add "HKEY_CLASSES_ROOT\exefile\shell\ColdClient\command" /ve /t REG_SZ /d "\"%mainBatPath%\" \"%%1\" \"3\"" /f
"%nircmdPath%" speak text "Added the cold client loader context menu for executable files"
reg add "HKEY_CLASSES_ROOT\exefile\shell\Remove Steam Stub" /v "Icon" /t REG_SZ /d "%steamStubIconPath%" /f
reg add "HKEY_CLASSES_ROOT\exefile\shell\Remove Steam Stub" /ve /t REG_SZ /d "ARMGDDN Steam Stub Remover" /f
reg add "HKEY_CLASSES_ROOT\exefile\shell\Remove Steam Stub\command" /ve /t REG_SZ /d "\"%mainBatPath%\" \"%%1\" \"1\"" /f
"%nircmdPath%" speak text "Added the steam stub check and remove context menu for executable files"
reg add "HKEY_CLASSES_ROOT\exefile\shell\VD bat" /v "Icon" /t REG_SZ /d "%vdBatIconPath%" /f
reg add "HKEY_CLASSES_ROOT\exefile\shell\VD bat" /ve /t REG_SZ /d "ARMGDDN VD Batmaker" /f
reg add "HKEY_CLASSES_ROOT\exefile\shell\VD bat\command" /ve /t REG_SZ /d "\"%mainBatPath%\" \"%%1\" \"2\"" /f
"%nircmdPath%" speak text "Added the VD Batmaker context menu for executable files for use with VR headsets"
echo Registry entries added successfully.
"%nircmdPath%" speak text "All context menu options added succesfully. Enjoy"
endlocal