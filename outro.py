from binance.exceptions import BinanceAPIException
from binance.client import Client
import json

api_key = 'T8mJdnXcyoijRGgQmjxvRyqxUAsWvnxpCX6BO4XQpwc8rFaYJHIn4fjzBdfki6Qi'
api_secret = '5vg6ij9eg8eBRWsQzmlsKHlHhLHNZwbmrW53y4NuuWikBeqxqx99AdzjX5sULJuQ'
    
def mainsell(quantity1,symbol1):
    
    client = Client(api_key=api_key, api_secret=api_secret)
    
    try:
        market_res = client.order_market_sell(symbol=symbol1, quantity=quantity1)
    except BinanceAPIException as e:
        print(e)
    else:
        print(json.dumps(market_res, indent=2))
    
    client.close_connection()

def mainbuy(quantity1,symbol1):
    
    client = Client(api_key=api_key, api_secret=api_secret)
    
    try:
        market_res = client.order_market_buy(symbol=symbol1, quantity=quantity1)
    except BinanceAPIException as e:
        print(e)
    else:
        print(json.dumps(market_res, indent=2))
    
    client.close_connection()
