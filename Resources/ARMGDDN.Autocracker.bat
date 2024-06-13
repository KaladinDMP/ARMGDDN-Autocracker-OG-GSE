@echo off
setlocal enabledelayedexpansion
set "droppedFile=%~1"
set "droppedDir=%~dp1"
set "fileName=%~n1"
set "extension=%~x1"
ren "%droppedFile%" "%fileName%.AG"

set "batchDir=%~dp0"
set "sourceFile=%batchDir%Api\%fileName%.dll"
set "destFile=%droppedDir%%fileName%.dll"
copy "%sourceFile%" "%destFile%" >nul 2>&1

set "appIdFile="
for /r "%droppedDir%" %%f in (steam_appid.txt) do (
    if exist "%%f" (
        set "appIdFile=%%f"
        goto :foundAppIdFile
    )
)
if "%appIdFile%"=="" (
    echo Running ARMGDDN.App.ID.exe...
    call "%~dp0AppID\ARMGDDN.App.ID.exe" "%droppedDir%"
    if exist "%~dp0AppID\steam_appid.txt" (
        echo Moving steam_appid.txt to "%droppedDir%"...
        move "%~dp0AppID\steam_appid.txt" "%droppedDir%"
        set "appIdFile=%droppedDir%\steam_appid.txt"
        goto :foundAppIdFile
    ) else (
        CLS
        echo Steam_appid.txt not found in "%~dp0AppID\, skipping move."
        echo Please enter the steam APP ID manually
        call :needAppId
    )
)
goto :eof

:foundAppIdFile
PAUSE
CLS
set /p appId=<"%appIdFile%"

echo Steam_appid.txt found!
echo App ID is: %appId%
goto :haveAppId

:needAppId
PAUSE
CLS
echo This next part requires the game's Steam app ID.
set /p needHelp="Do you need help finding the app ID? (Y/N): "
if /i "%needHelp%"=="Y" (
    start "" "https://www.youtube.com/watch?v=XHQT7a-ORFk"
) else if /i "%needHelp%"=="Yes" (
    start "" "https://www.youtube.com/watch?v=XHQT7a-ORFk"
)
cls
set /p appId="Enter the game's app ID: "

:haveAppId
cls
echo App ID recorded successfully: %appId%

echo Creating steam_settings folder next

pause
cls
"%batchDir%ARMGDDN.Steam.Settings.exe" %appId%
echo Script Complete
pause
exit /b 0