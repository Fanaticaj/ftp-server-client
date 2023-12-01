@echo off

:: Get the current directory
set CURRENT_DIR=%cd%

:: Start the server script in a new cmd window in the current directory
start cmd /k "cd /D %CURRENT_DIR% && py ftp-server-simple.py 1000"

:: Sleep for 2 seconds to give the server time to start up
timeout /t 2 >nul

:: Start the client script in another cmd window in the current directory
start cmd /k "cd /D %CURRENT_DIR% && py ftp-client-simple.py 1000"

exit
