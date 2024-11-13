import requests
import json
import datetime

from multiprocessing import Pool
from bs4 import BeautifulSoup

with open('items.json', 'r') as f:
	_items = json.loads(f.read())

def _get_item_nameid(market_hash_name: str, APPID=730):
	global _items

	item_nameid = _items['cs'].get(market_hash_name)
	if (item_nameid):
		return item_nameid

	res = requests.get(f'https://steamcommunity.com/market/listings/{APPID}/{market_hash_name}/')

	if (res.status_code != 200):
		print("Sleep and try later")
		return None

	soup = BeautifulSoup(res.text, 'html.parser')
	last_script = str(soup.find_all('script')[-1])

	last_script_token = last_script.split('(')[-1]
	item_nameid = int(last_script_token.split(');')[0])

	_items['cs']['market_hash_name'] = str(item_nameid)
	with open('items.json', 'w') as f:
		f.write(json.dumps(_items))

	return item_nameid

def get_history(hash_name: str, APPID=730):
	url = f"https://steamcommunity.com/market/listings/{APPID}/\{\}"

	r = requests.get(url.format(hash_name))
	if (r.status_code != 200):
		return list()

	start = r.text.find('var line1=')
	raw_history = json.loads(r.text[start + 10 : start + r.text[start:].find(']]') + 2]) # 10 - 'var line1=' size

	for i, el in enumerate(raw_history):
		raw_history[i][0] = datetime.datetime.strptime(el[0][:14], '%b %d %Y %H') # Feb 18 2016 01: +0

	history = raw_history

	return (history)

def _get_item_histogram(item_nameid: int, currency=1):
	url = f"https://steamcommunity.com/market/itemordershistogram?country=US&language=english&currency={currency}&item_nameid={item_nameid}&two_factor=0"

	res = requests.get(url)
	print(res.text)
	if (res.status_code != 200):
		print("Sleep and try later")
		return None

	return res.json()

def _get_buy_sell_orders(market_hash_name: str):
	item_nameid = _get_item_nameid(market_hash_name)

	histogram = _get_item_histogram(item_nameid)
	if (histogram is None):
		return (None, None)

	if (len(histogram['buy_order_graph']) == 0 or
		len(histogram['sell_order_graph']) == 0):
		return (None, None)

	return (histogram['buy_order_graph'], histogram['sell_order_graph'])

def _get_delta(market_hash_name: str):
	# Return delta from buy by sell in percent
	buy_orders, sell_orders = _get_buy_sell_orders(market_hash_name)
	if ((buy_orders is None) or (sell_orders is None)):
		return None

	return (sell_orders[0][0] / buy_orders[0][0])

def _mass_get_delta(item_list: list[str]):
	with Pool(5) as _pool:
		result = _pool.map(_get_delta, item_list)

	delta = {}
	i = 0
	for item in item_list:
		delta[item] = result[i]
		i += 1

	return delta


def main():
	global _items

	item_list = list(_items['cs'].keys())

	index = 200
	print(f"Item={item_list[index]}, delta={_get_delta(item_list[index])}")
	# while 1:
	# 	index += 5
	# 	data = _mass_get_delta(item_list[index:index+5])
	# 	pretty_data = json.dumps(data, indent=4)

	# print(pretty_data)

if __name__ == '__main__':
	main()

