import threading
from env import api_key,api_secret
import ccxt


class Filter(threading.Thread):
    def __init__(self, Vmin, coin, exchange, orderbook, lock,main):
        super().__init__()
        # create websocket connection
        self.orderbook = orderbook
        self.lock = lock
        exchange = ccxt.binance(main)

        volumes = []

        vls = exchange.fetchTickers()
        
        markets = vls.keys()

        market_symbols = (list(markets))

        def FilterV3(sym1): 
            sym1_token1 = sym1.split('/')[0]
            sym1_token2 = sym1.split('/')[1]
            if (sym1_token2 == 'USDT'):
                ticker = vls[sym1]
                x = float(ticker['quoteVolume'])
                if (x > Vmin):
                    return sym1
            if (sym1_token2 == 'BUSD'):
                ticker = vls[sym1]
                x = float(ticker['quoteVolume'])
                if (x > Vmin):
                    return sym1
            if (sym1_token2 == 'USDC'):
                ticker = vls[sym1]
                x = float(ticker['quoteVolume'])
                if (x > Vmin):
                    return sym1
            if (sym1_token2 == 'DAI'):
                ticker = vls[sym1]
                x = float(ticker['quoteVolume'])
                if (x > Vmin):
                    return sym1    
            if (sym1_token2 == 'TUSD'):
                ticker = vls[sym1]
                x = float(ticker['quoteVolume'])
                if (x > Vmin):
                    return sym1
            if (sym1_token1 == 'USDT'):
                ticker = vls[sym1]
                x = float(ticker['baseVolume'])      
                if (x > Vmin):
                    return sym1
            if (sym1_token1 == 'BUSD'):
                ticker = vls[sym1]
                x = float(ticker['baseVolume'])        
                if (x > Vmin):
                    return sym1
            if (sym1_token1 == 'USDC'):
                ticker = vls[sym1]
                x = float(ticker['baseVolume'])        
                if (x > Vmin):
                    return sym1
            if (sym1_token1 == 'DAI'):
                ticker = vls[sym1]
                x = float(ticker['baseVolume'])        
                if (x > Vmin):
                    return sym1
            if (sym1_token1 == 'BTC'):
                ticker = vls[sym1]
                x = float(ticker['baseVolume'])
                ticker_btc = vls['BTC/USDT']
                order_btc = float(ticker_btc['close'])        
                vol = x * order_btc
                if (vol > Vmin):
                    return sym1
            if (sym1_token1 == 'ETH'):
                ticker = vls[sym1]
                x = float(ticker['baseVolume'])        
                ticker_eth = vls['ETH/USDT']
                order_eth = float(ticker_eth['close'])
                vol = x * order_eth
                if (vol > Vmin):
                    return sym1
            if (sym1_token1 == 'BNB'):
                ticker = vls[sym1]
                x = float(ticker['baseVolume'])        
                ticker_bnb = vls['BNB/USDT']
                order_bnb = float(ticker_bnb['close'])
                vol = x * order_bnb
                if (vol > Vmin):
                    return sym1
            if (sym1_token2 == 'BTC'):
                ticker = vls[sym1]
                x = float(ticker['quoteVolume'])
                ticker_btc = vls['BTC/USDT']
                order_btc = float(ticker_btc['close'])
                vol = x * order_btc
                if (vol > Vmin):
                    return sym1
            if (sym1_token2 == 'ETH'):
                ticker = vls[sym1]
                x = float(ticker['quoteVolume'])
                ticker_eth = vls['ETH/USDT']
                order_eth = float(ticker_eth['close'])
                vol = x * order_eth
                if (vol > Vmin):
                    return sym1
            if (sym1_token2 == 'BNB'):
                ticker = vls[sym1]
                x = float(ticker['quoteVolume'])
                ticker_bnb = vls['BNB/USDT']
                order_bnb = float(ticker_bnb['close'])
                vol = x * order_bnb
                if (vol > Vmin):
                    return sym1
            if (sym1_token2 == 'EUR'):
                ticker = vls[sym1]
                x = float(ticker['quoteVolume'])
                if (x > Vmin):
                    return sym1
            if (sym1_token2 == 'GBP'):
                ticker = vls[sym1]
                x = float(ticker['quoteVolume'])
                if (x > Vmin):
                    return sym1
                    
        for symbol in market_symbols:
            for idx,char in enumerate(symbol):
                # print(char)
                if char == "/":
                    if FilterV3(symbol) != None:
                        volumes.append(FilterV3(symbol))

        # print(volumes)
        def get_crypto_combinations(market_symbols, base):
            combinations = []
            for sym1 in market_symbols:
                sym1_token1 = sym1.split('/')[0]
                sym1_token2 = sym1.split('/')[1]
                if (sym1_token2 == base):
                    for sym2 in market_symbols:
                        sym2_token1 = sym2.split('/')[0]
                        sym2_token2 = sym2.split('/')[1]
                        if (sym1_token1 == sym2_token2):
                            for sym3 in market_symbols:
                                sym3_token1 = sym3.split('/')[0]
                                sym3_token2 = sym3.split('/')[1]
                                if ((sym2_token1 == sym3_token1) and (sym3_token2 == sym1_token2)):
                                    combination = {
                                        'base': sym1_token2,
                                        'intermediate': sym1_token1,
                                        'ticker': sym2_token1,
                                    }
                                    self.orderbook.append(combination)
                                    combinations.append(combination)
                                    
            return combinations

        # get_crypto_combinations(volumes, coin)
        # print(wx_combinations_coin)
    
        wx_combinations_coin0 = get_crypto_combinations(volumes, coin[0])
        #wx_combinations_coin1 = get_crypto_combinations(volumes, coin[1])

        print(f"fazendo filter para {coin[0]}")
        #print(f"fazendo filter para {coin[1]} ")
        print(f'No. of crypto combinations: {len(wx_combinations_coin0)}')
        