# Simple Bot for search and find python packages
Simple but effective bot to search Python packages in pypi.org, the results are displayed in order of list hoping that they are useful to you. 
This bot used a web scraping with a local API.

# How to run?
Use the command
> `python bot_telegram.py` 
# What do you need?
All Python packages used in this bot are in the file: 
> `requirements.txt`
## How to install all Python packages? 
> `pip install [package] or [package]==[version]` 
# UI and Messages
The first message send to user has information about of bot

<img src="img/start.jpg" width="40%" height="40%">

When the user presses start these options are displayed, choose a language. 

<img src="img/select_lang.jpg" width="40%" height="40%">

Depends on the option selected, displays the welcome message.

<img src="img/welcome_mesage.jpg" width="40%" height="40%">

For search package select "Search Package or Buscar Package" and typing the PP.
This screen displays the first page of pypi results.

<img src="img/search_page1.jpg" width="40%" height="40%">

If selected "More results or Más resultados", will display the results for second page.

<img src="img/search_page2.jpg" width="40%" height="40%">

<img src="img/results_page2.jpg" width="40%" height="40%">

If you need change lang, select "Change lang and Restart or Cambiar idioma y reiniciar"

<img src="img/change_lang_options.jpg" width="40%" height="40%">

If you need restart bot, typing /start command or select this option in the menu.

<img src="img/start_command.jpg" width="40%" height="40%">

# Resources

Telegram: https://core.telegram.org/bots/api

Bot Telegram: https://python-telegram-bot.readthedocs.io/en/stable/index.html

Emojis: https://unicode.org/emoji/charts/full-emoji-list.html

Pyshortener: https://pyshorteners.readthedocs.io/en/latest/

Googletrans: https://py-googletrans.readthedocs.io/en/latest/

BS4: https://www.crummy.com/software/BeautifulSoup/bs4/doc/