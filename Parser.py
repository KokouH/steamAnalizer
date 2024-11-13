
import requests
import datetime
import json

class Parser:
    def __init__(self) -> None:
        self.last_page = None
        self.ses = requests.Session()

    def get_itemid_from_page(self, page: str):
        if page == None:
            return None
        x = page.find('Market_LoadOrderSpread(') + 24
        return int(page[x: x  + page[x:].find(' ')])

    def get_item_page(self, hash_name: str, appid: int = 252490):
        res = self.ses.get(f'https://steamcommunity.com/market/listings/{appid}/{hash_name}')
        if res.status_code != 200:
            self.last_page = res.text
            return None
        self.last_page = res.text
        return res.text
    
    def get_item_histogram(self, itemid: int):
        res = self.ses.get(f'https://steamcommunity.com/market/itemordershistogram?country=US&language=english&currency=1&item_nameid={itemid}')
        if res.status_code != 200:
            return None
        
        return res.json()
    
    def get_history(self, page: str):
        start = page.find('var line1=')
        raw_history = json.loads(page[start + 10 : start + page[start:].find(']]') + 2]) # 10 - 'var line1=' size

        for i, el in enumerate(raw_history):
            raw_history[i][0] = datetime.datetime.strptime(el[0][:14], '%b %d %Y %H') # Feb 18 2016 01: +0

        history = raw_history

        return (history)