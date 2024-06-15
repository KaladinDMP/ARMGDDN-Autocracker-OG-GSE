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
"%nircmdPath%" speak text "Removing Armageddon Auto Cracker context menu options."
"%nircmdPath%" trayballoon "ARMGDDN Autocracker" "Removing ARMGDDN Autocracker context menu options for executable and .dll files." "D:\Downloads\goldberg\ARMGDDNAutocracker\Resources\ARMGDDN.Autocracker.exe" 5000
echo Removing registry entries...
"%nircmdPath%" speak text "Removing registry entries."
reg delete "HKEY_CLASSES_ROOT\dllfile\shell\AutoCracker" /f
"%nircmdPath%" speak text "Removed the autocracker context menu for steam API dll files"
reg delete "HKEY_CLASSES_ROOT\dllfile\shell\SteamInterfaces" /f
"%nircmdPath%" speak text "Removed the autocracker context menu for steam interface from original steam API dll files"
reg delete "HKEY_CLASSES_ROOT\exefile\shell\AutoCracker" /f
"%nircmdPath%" speak text "Removed the autocracker context menu for executable files"
reg delete "HKEY_CLASSES_ROOT\exefile\shell\ColdClient" /f
"%nircmdPath%" speak text "Removed the cold client loader context menu for executable files"
reg delete "HKEY_CLASSES_ROOT\exefile\shell\Remove Steam Stub" /f
"%nircmdPath%" speak text "Removed the steam stub check and remove context menu for executable files"
reg delete "HKEY_CLASSES_ROOT\exefile\shell\VD bat" /f
"%nircmdPath%" speak text "Removed the VD Batmaker context menu for executable files"
echo Registry entries removed successfully.
"%nircmdPath%" speak text "All context menu options removed successfully. Good Bye"
endlocal