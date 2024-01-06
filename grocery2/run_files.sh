# Open a new terminal window and execute the commands
osascript -e 'tell application "Terminal" to do script "cd Documents/Grocery2/backendcode && python3.9 app.py"'
osascript -e 'tell application "Terminal" to do script "cd Documents/Grocery2/frontendcode && npm run serve"'
osascript -e 'tell application "Terminal" to do script "redis-server"'
osascript -e 'tell application "Terminal" to do script "cd Documents/Grocery2/backendcode && python3.9 reminders.py"'
osascript -e 'tell application "Terminal" to do script "cd Documents/Grocery2/backendcode && celery -A tasks.celery worker --loglevel=info"'
osascript -e 'tell application "Terminal" to do script "cd Documents/Grocery2/backendcode && celery -A tasks.celery beat"'