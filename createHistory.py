
import json
from config import *
from Parser import Parser
from steampy.client import SteamClient, GameOptions

with open(STEAM_PATH_COOKIES, 'r') as file:
    login_cookies = json.loads(file.read())
steam_client = SteamClient(STEAM_API_KEY, username=STEAM_LOGIN, login_cookies=login_cookies)

assert steam_client.was_login_executed

r = steam_client._session.get('https://steamcommunity.com/market/myhistory?count=500&norender=1')

if r.status_code != 200:
    print("Can't get hisotry ;(")
    exit()

with open('history.json', 'w') as file:
    file.write( json.dumps(r.json()) )

print("History saved.")
