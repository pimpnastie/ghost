@echo off
title Build Discloud Zip
cd /d "%~dp0"
echo Packaging files into fortnite-bot-discloud.zip...
powershell -Command "Compress-Archive -Path bot.py, fortnite_client.py, embed_builder.py, config.py, database.py, requirements.txt, discloud.config, .env -DestinationPath fortnite-bot-discloud.zip -Force"
echo Done! Upload fortnite-bot-discloud.zip to Discloud dashboard.
pause
