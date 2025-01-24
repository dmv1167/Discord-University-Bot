# Discord University Bot
A multi-purpose discord bot written with the intent to aid university students with bus schedules handled by the tracking service PassioGo

# Usage
You will need to populate the .env file with your Discord API key and other required PassioGo and customization information.
If you wish to webscrape your university's bus schedule website, bot.py:3 and bus.py:17,23 need comments removed, as well as the functions responsible for retrieving the info. You will need to implement the scraping as all websites are different.

# Bus API
The bus data accessed by this bot is made possible by [this repository](https://github.com/athuler/PassioGo)
