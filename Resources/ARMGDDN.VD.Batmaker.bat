@echo off
setlocal enableExtensions disableDelayedExpansion
echo                            _____ __________    _____    ________________  ________    _______   
echo                           /  _  \\______   \  /     \  /  _____/\______ \ \______ \MP \      \  
echo                          /  /_\  \^|       _/ /  \ /  \/   \  ___ ^|    ^|  \ ^|    ^|  \  /   ^|   \ 
echo                         /    ^|    \    ^|   \/    Y    \    \_\  \^|    `   \^|    `   \/    ^|    \
echo                         \____^|__  /____^|_  /\____^|__  /\______  /_______  /_______  /\____^|__  /
echo                                 \/       \/         \/        \/        \/        \/         \/ 
echo.
echo. 
set "extension=%~x1"

if /i not "%extension%"==".exe" (
    echo WARNING: The file must be an EXE
    echo.
    echo NOW EXITING...
    echo.
    pause
    exit /b 1
)

set /p cstm=Type in any needed arguments or just hit enter for none (EG:"-VR -Windowed", no quotes): 
echo.
echo.
echo Arguments set!
echo.
echo.
TIMEOUT /T 3

echo "C:\Program Files\Virtual Desktop Streamer\VirtualDesktop.Streamer.exe" "%~nx1" ^%cstm% > VD.bat
goto :end

:end
endlocal
