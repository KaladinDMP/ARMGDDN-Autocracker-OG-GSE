@echo off
SETLOCAL
set "extension=%~x1"

if /i not "%extension%"==".exe" (
    echo WARNING: The file must be an EXE
    echo.
    echo NOW EXITING...
    echo.
    pause
    exit /b 1
)

set steamless="%~dp0SteamlessCLI\Steamless.CLI.exe"
 
%steamless% --keepbind %1
%~d1
CD %~dp1
IF EXIST "%~dp1\%~nx1.unpacked.exe" (
  REN %1 "%~n1.AG"
  REN "%~nx1.unpacked.exe" "%~nx1"
)
Pause