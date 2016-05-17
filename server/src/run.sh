(crontab -u pi -l ; echo "* * * * *  python serie/serie.py") | crontab -u pi -
python server.py&
python ../bot/src/main/DomoticBot.py&

