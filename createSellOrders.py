
import json
import time
import math
from config import *
from Parser import Parser
from steampy.client import SteamClient, GameOptions

def main():
    if STEAM_PATH_COOKIES:
        with open(STEAM_PATH_COOKIES, 'r') as file:
            login_cookies = json.loads(file.read())
        if STEAM_PATH_GUARD:
            print("Try login with guard")
            steam_client = SteamClient(STEAM_API_KEY)
            steam_client.login(STEAM_LOGIN, STEAM_PASSWORD, STEAM_PATH_GUARD)
        else:
            steam_client = SteamClient(STEAM_API_KEY, username=STEAM_LOGIN, login_cookies=login_cookies)
    else:
        steam_client = SteamClient(STEAM_API_KEY)

    assert steam_client.was_login_executed

    with open("goods", 'r') as file:
        items = file.read().split('\n')
        items = [i.split(':') for  i in items]
    parser = Parser()

    sell_prices = {}
    for item in items:
        sell_prices[item[0]] = item[1]

    inventory = steam_client.get_my_inventory(GameOptions.RUST)
    item_ids = list(inventory.keys())

    for id in item_ids:
        if inventory[id]['marketable'] != 1:
            print(f"{inventory[id]['name']} not marketable")
            continue

        if inventory[id]['name'] in sell_prices:
            sell_price = round(sell_prices[inventory[id]['name']] * 87)
        else:
            parser.get_item_page(inventory[id]['name'])
            itemId = parser.get_itemid_from_page(parser.last_page)
            histogram = parser.get_item_histogram(itemId)
            if parser.last_page is None or histogram is None:
                continue
            sell_price = round(histogram['sell_order_graph'][0][0] * 87)

        sell_price = str(sell_price)
        sell_response = steam_client.market.create_sell_order(id, GameOptions.RUST, sell_price)

        print(sell_response)

        time.sleep(2)

if __name__ == "__main__":
    main()