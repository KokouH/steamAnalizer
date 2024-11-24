
import datetime
import json
import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from Parser import Parser
from Validator import Validator

# Main params
min_sells_per_month = 60
wanted_profit = 10
max_deeps = 7
trend_max = 1.15
trend_min = 0.95
sell_conf = 0.1

# Spike clean params
WINDOW_SIZE = 10
THRESHOLD_MULTIPLIER = 2.5

def remove_spikes(history):
    df = pd.DataFrame([i[1] for i in history], columns=['Value'])
    window_size = WINDOW_SIZE
    threshold_multiplier = THRESHOLD_MULTIPLIER 

    df['Rolling_Mean'] = df['Value'].rolling(window=window_size).mean()
    df['Rolling_Std'] = df['Value'].rolling(window=window_size).std()
    df['Spike'] = (df['Value'] > (df['Rolling_Mean'] + threshold_multiplier * df['Rolling_Std'])) | \
                (df['Value'] < (df['Rolling_Mean'] - threshold_multiplier * df['Rolling_Std']))
    clean_history = []
    for i, val in enumerate(df['Spike']):
        if not val:
            clean_history.append(history[i])
    return clean_history

def  get_last_month(history):
    last_history = []
    now_datetime = datetime.datetime.now()
    delta = datetime.timedelta(days=30)
    for i in reversed(history):
        if now_datetime - i[0] > delta:
            break;
        last_history.append(i)

    return list(reversed(last_history))

def check_sells_count(data):
    history = get_last_month(data['history'])
    history = remove_spikes(history)
    sells = 0
    for i in history:
        sells += int(i[2])
    
    return sells >= min_sells_per_month

def check_deep_in_cup(data):
    reference_price = data['reference_price'] * .87 * (1 - wanted_profit / 100)
    count = 0
    for i in data['histogram']['buy_order_graph']:
        count += i[1]
        if (reference_price >= i[0]):
            break;
    
    sells = 0
    for i in get_last_month(data['history']):
        sells += int(i[2])

    return count * 30 / sells <= max_deeps

def check_price_trend(data):
    history = get_last_month(data['history'])
    history = remove_spikes(history)

    # Пример данных
    y = np.array([i[1] for i in  history])
    x = np.array([i for i in range(len(history))])

    z = np.polyfit(x, y, 1)
    p = np.poly1d(z)
    m = p(x[-1]) / p(x[0])

    return m < trend_max and m > trend_min

def check_sell_in_history(data):
    history = get_last_month(data['history'])
    history = remove_spikes(history)

    all_sells = 0
    for i in history:
        all_sells += int(i[2])

    above_sells = 0
    for i in history:
        if i[1] >= data['reference_price']:
            above_sells += int(i[2])

    return above_sells / all_sells > 

def main():
    good_file = open('goods', 'w')
    bad_file = open('bad', 'w')

    TEST_ITEM = 'Raven Poncho'

    with open('rust.json', 'r') as file:
        item_hash_names = [item['hash_name'] for item in json.loads(file.read())]

    parser = Parser()
    validator = Validator([
        check_sells_count,
        check_price_trend,
        check_deep_in_cup,

    ])

    for TEST_ITEM in item_hash_names:
        parser.get_item_page(TEST_ITEM)
        itemId = parser.get_itemid_from_page(parser.last_page)
        if parser.last_page == None or itemId == None:
            time.sleep(90)
            continue
        histogram = parser.get_item_histogram(itemId)
        history = parser.get_history(parser.last_page)
        buy_price = data['reference_price'] * .87 * (1 - wanted_profit /  100)
        data = {
            'history': history,
            'histogram': histogram,
            'reference_price': histogram['sell_order_graph'][0][0],
            'buy_price': buy_price,
        }

        if validator.validate(data):
            print(f"Nice {TEST_ITEM}")
            print(f"Sell price: {data['reference_price']}")
            print(f"Buy order: {buy_price}")
            good_file.write(f"{TEST_ITEM}:{data['reference_price']}:{buy_price}\n")
            good_file.flush()
        else:
            print(f"Bad item {TEST_ITEM}")
            bad_file.write(f"{TEST_ITEM}\n")
            bad_file.flush()

        time.sleep(10)

    bad_file.close()
    good_file.close()

if __name__ == "__main__":
    main()