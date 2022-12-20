import threading
from env import api_key,api_secret
import ccxt
from binance.exceptions import BinanceAPIException

def funcao(): 
    exchange = "Filter"

    lock = threading.Lock()
    symbolfilter = []
    orderbook = symbolfilter

    main = {
    "apiKey": api_key,
    "secret": api_secret,
    'enableRateLimit': True,
    # "verbose": True,
    }

    exchange = ccxt.binance(main)
    volumes = []
    vls = exchange.fetchTickers()
    markets = vls.keys()
    market_symbols = (list(markets))
    bitcoins = []

    for i in range(0,len(market_symbols)):
        if market_symbols[i][0:4] == "BTC/": 
            bitcoins.append({'symbol': market_symbols[i], 'id': 1})
        if market_symbols[i][len(market_symbols[i])-3:len(market_symbols[i])] == "BTC": 
            bitcoins.append({'symbol': market_symbols[i], 'id': 0})
    
    return bitcoins


#pega os valores e coloca os simbolos de cada

#coloca os ids de cada



#id é 1 quando começa com bitcoin
#id é 0 quando termina com bitcoin
#----------------------------------------------------


