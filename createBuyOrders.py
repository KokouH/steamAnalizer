
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
        steam_client = SteamClient(STEAM_API_KEY, username=STEAM_LOGIN, login_cookies=login_cookies)
    else:
        steam_client = SteamClient(STEAM_API_KEY)

    assert  
    with open("goods", 'r') as file:
        items = file.read().split('\n')
        items = [i.split(':') for  i in items]
    parser = Parser()
    start_item = 'Space Raider Helmet'
    while items[0][0] != start_item:
        del(items[0])

    current_balance = 95
    current_balance *= 9
    car = current_balance / len(items)
    print(f"Start item: {items[0]}")
    for item in items:
        if not item:
            continue;
        success = False
        while not success:
            parser.get_item_page(item[0])
            itemid =  parser.get_itemid_from_page(parser.last_page)
            histogram = parser.get_item_histogram(itemid)
            if parser.last_page == None or histogram == None:
                time.sleep(90)
                continue

            buy_price = float(item[2])
            if histogram['buy_order_graph'][0][0] < buy_price:
                buy_price = histogram['buy_order_graph'][0][0]

            try:
                response = steam_client.market.create_buy_order(
                    market_name=item[0],
                    price_single_item=str(int(buy_price * 100) + 1),
                    quantity=math.ceil(car / buy_price),
                    game=GameOptions.RUST
                )
                buy_order_id = response["buy_orderid"]
                print(f"{item[0]} buy price: {buy_price}, order: {buy_order_id}")
            except:
                print(response)
                continue;
            success = True

        time.sleep(10)

if __name__ == "__main__":
    main()