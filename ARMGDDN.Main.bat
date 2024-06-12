@echo off
echo Processing file: "%~1"
echo.
set "droppedFile=%~1"
set "droppedDir=%~dp1"
set "fileName=%~n1"
set "fileExt=%~x1"
set "userChoice=%~2"
if "%droppedFile%"=="" (
    echo No file was dropped onto the script
    echo Please drag and drop an EXE or DLL file onto the script to process it
    echo OR use the context menu registry files in the main folder.
    pause
    exit /b
)
echo Searching for steam_appid.txt...
set "appIdFile="
for /r "%droppedDir%" %%f in (steam_appid.txt) do (
    if exist "%%f" (
        set "appIdFile=%%f"
        for /f "usebackq delims=" %%i in ("%%f") do set "appId=%%i"
        set "appId=%appId: =%"
        echo Moving steam_appid.txt to "%droppedDir%"...
        move "%%f" "%droppedDir%"
    )
)

if /i "%fileExt%"==".exe" (
    echo Entering EXE processing block...
    goto exe_menu
) else if /i "%fileExt%"==".dll" (
    if /i not "%fileName%%fileExt%"=="steam_api64.dll" if /i not "%fileName%%fileExt%"=="steam_api.dll" (
        CLS
        echo WARNING: The dll file must be either steam_api64 or steam_api.
        echo.
        echo NOW EXITING...
        echo.
        pause
        exit /b 1
    )
    echo The dropped file is a DLL.
    echo.
    echo Running ARMGDDN.Autocracker.exe...
    call "%~dp0Resources\ARMGDDN.Autocracker.exe" "%droppedFile%"
) else (
    echo Unsupported file type. Please drop an EXE or DLL file. 
    echo.
    pause
    exit /b
)
goto end
:exe_menu
PAUSE
CLS
if "%userChoice%"=="1" (
    echo Running ARMGDDN.Stub.Remover.exe...
    call "%~dp0Resources\ARMGDDN.Stub.Remover.exe" "%droppedFile%"
    goto end
) else if "%userChoice%"=="2" (
    echo Running ARMGDDN.VD.Batmaker.exe...
    call "%~dp0Resources\ARMGDDN.VD.Batmaker.exe" "%droppedFile%"
    if exist "%~dp0VD.bat" (
        move "%~dp0VD.bat" "%droppedDir%"
    ) else (
        echo VD.bat not found in "%~dp0"
    )
    goto end
) else if "%userChoice%"=="3" (
    echo Running ARMGDDN.Cold.Client.exe
    call "%~dp0Resources\ARMGDDN.Cold.Client.exe" "%droppedFile%"
    goto end
)
CLS
echo Please select the script to run:
echo.
echo 1. Check for and remove a steam stub
echo.
echo 2. VD bat for Virtual Desktop owners - VR ONLY
echo.
echo 3. ColdClient_Loader Crack
echo.
echo 4. Quit
echo.
set /p choice="Enter your choice (1-4): "
CLS
if "%choice%"=="1" (
    echo Running ARMGDDN.Stub.Remover.exe...
    call "%~dp0Resources\ARMGDDN.Stub.Remover.exe" "%droppedFile%"
    goto exe_menu
) else if "%choice%"=="2" (
    echo Running ARMGDDN.VD.Batmaker.exe...
    call "%~dp0Resources\ARMGDDN.VD.Batmaker.exe" "%droppedFile%"
    if exist "%~dp0VD.bat" (
        move "%~dp0VD.bat" "%droppedDir%"
    ) else (
        echo VD.bat not found in "%~dp0"
    )
    goto exe_menu
) else if "%choice%"=="3" (
    echo Running ARMGDDN.Cold.Client.exe
    call "%~dp0Resources\ARMGDDN.Cold.Client.exe" "%droppedFile%" "%appId%"
    goto exe_menu
) else if "%choice%"=="4" (
    echo Quitting...
    goto end
) else (
    echo Invalid choice. Please try again.
    goto exe_menu
)
pause
:end