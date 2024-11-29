
import json

'''
event_types
4 - buyed
3 - selled
'''

start_timestamp = 1731467755

class Item:
    def __init__(self):
        self.name = ''
        self.buy_price = -1
        self.sell_price = -1

with open("history.json", 'r') as file:
    data = json.loads(file.read())

output = []
assets = data['assets']['252490']['2']

for event in data['events']:
    if event['event_type'] != 4:
        continue;
    
    if event['time_event'] < start_timestamp:
        continue;

    asset_id = data['listings'][event['listingid']]['asset']['id']
    if (asset_id not in assets):
        continue
    name = assets[ asset_id ]['name']

    purchase = data['purchases'][f"{event['listingid']}_{event['purchaseid']}"]
    buy_price = purchase['paid_amount'] + purchase['paid_fee']
    sell_price = 0

    item = Item()
    item.name = name
    item.buy_price = buy_price
    
    output.append(item)

for event in data['events']:
    if event['event_type'] != 3:
        continue;
    
    if event['time_event'] < start_timestamp:
        continue;

    asset_id = data['listings'][event['listingid']]['asset']['id']
    if (asset_id not in assets):
        continue
    name = assets[ asset_id ]['name']

    purchase = data['purchases'][f"{event['listingid']}_{event['purchaseid']}"]
    sell_price = purchase['received_amount'] 

    for it in output:
        if name == it.name:
            if it.sell_price == -1:
                it.sell_price = sell_price

def nice_print(item, sizes=[10, 4, 4, 5, 5]):
    output = [
        item.name,
        str(item.buy_price),
        str(item.sell_price),
        str((item.sell_price / item.buy_price - 1) * 100),
        '' if item.buy_price <= item.sell_price else "MINUS"
    ]

    for i in range(len(output)):
        if len(output[i]) < sizes[i]:
            output[i] += sizes[i] * ' '

        output[i] = output[i][:sizes[i]]

    print(' | '.join(output))

all_buy = 0
all_sell = 0
sizes = [0, 4, 4, 5, 5]
sizes[0] = max(len(i.name) for i in output)

use_filter = True

for item in output:

    if item.sell_price > 0 or not use_filter:
        nice_print(item, sizes)
        all_buy += item.buy_price
        all_sell += item.sell_price

print(f"Profit: {all_buy * (all_sell / all_buy - 1) / 100} {(all_sell / all_buy - 1)}")


