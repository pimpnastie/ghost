@echo off
title Stop Fortnite Discord Bot
echo Stopping any running bot instances...
taskkill /F /FI "WINDOWTITLE eq Fortnite Discord Bot" /T >nul 2>&1
wmic process where "commandline like '%%fortnite-discord-bot\\bot.py%%'" call terminate >nul 2>&1
echo Bot stopped.
pause
