@echo off
setlocal enabledelayedexpansion
set "droppedFile=%~1"
set "droppedDir=%~dp1"
set "fileName=%~n1"
set "extension=%~x1"
set "batchDir=%~dp0"
set "sourceDir=%batchDir%Client"
set "destDir=%droppedDir%"
xcopy "%sourceDir%\*" "%destDir%" /s /e /y >nul

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
        
        echo Steam_appid.txt not found in "%~dp0AppID\, skipping move."
        echo Please enter the steam APP ID manually
        call :needAppId
    )
)
goto :eof
:foundAppIdFile
PAUSE

set /p appId=<"%appIdFile%"
echo Steam_appid.txt found!
echo App ID is: %appId%
goto :haveAppId
:needAppId
PAUSE

echo This next part requires the game's Steam app ID.
set /p needHelp="Do you need help finding the app ID? (Y/N): "
if /i "%needHelp%"=="Y" (
    start "" "https://www.youtube.com/watch?v=XHQT7a-ORFk"
) else if /i "%needHelp%"=="Yes" (
    start "" "https://www.youtube.com/watch?v=XHQT7a-ORFk"
)

set /p appId="Enter the game's app ID: "
:haveAppId
set "iniFile=%droppedDir%ColdClientLoader.ini"
set "exeLine=exe=%~nx1"
set "appIdLine=AppId=%appId%"

echo App ID recorded successfully: %appId%
echo.
pause

set /p args="Enter any arguments needed (leave blank and hit enter for none): "
set "newIniFile=%droppedDir%ColdClientLoader_new.ini"
(
    set "lineNum=0"
    for /f "usebackq tokens=1* delims=:" %%i in (`findstr /n "^" "%iniFile%"`) do (
        set /a lineNum+=1
        set "line=%%j"
        if !lineNum! equ 3 (
            echo !exeLine!
        ) else if !lineNum! equ 5 (
            if "!args!"=="" (
                echo ExeCommandLine=
            ) else (
                echo ExeCommandLine=!args!
            )
        ) else if !lineNum! equ 7 (
            echo !appIdLine!
        ) else (
            echo !line!
        )
    )
) > "%newIniFile%"
move /y "%newIniFile%" "%iniFile%" >nul

Echo ColdClientLoader.ini edited successfully
echo Creating steam_settings folder next

pause

"%batchDir%ARMGDDN.Steam.Settings.exe" %appId%
echo Script Complete
pause
exit /b 0