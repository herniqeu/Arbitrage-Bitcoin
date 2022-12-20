import ccxt
import math
import time
from env import api_key_testnet, api_secret_testnet, api_key, api_secret
from datetime import datetime
from filter import Filter
from chain import Chain
from order import Order
import threading
from binance.client import Client
from binance import Client
import requests
import math
from json import load
from all_book_ticker import Chain
from user_data_test import Order
from cancel_orders import Cancel
import time
from newfilter import *
from binance.enums import *
from outro import *
import json

client = Client(api_key, api_secret)

test = {
    "apiKey": api_key_testnet,
    "secret": api_secret_testnet,
    'enableRateLimit': True,
    # "verbose": True,
}
main = {
    "apiKey": api_key,
    "secret": api_secret,
    'enableRateLimit': True,
    # "verbose": True,
}
exchange = ccxt.binance(main)

exchange.set_sandbox_mode(enabled=False)

params = {
    'test': True,  # test if it's valid, but don't actually place it
}

def get_symbol_info(symbol): 
    data_from_api = client.get_symbol_info(symbol)
    return (data_from_api["orderTypes"])

def get_symbol_infothers(symbol): 
    data_from_api = client.get_symbol_info(symbol)
    return (data_from_api)

def assetbalance(symbol): 
    balance = client.get_asset_balance(asset=symbol)
    return balance

def getBOOK(symbol):
    return orderbooks[symbol]

def getBOOKask(symbol):
    if getBOOK(symbol) != None:
        ask = orderbooks[symbol]
        return ask['ask']
    else:
        None

def getBOOKbid(symbol):
    if getBOOK(symbol) != None:
        ask = orderbooks[symbol]
        return ask['bid']
    else:
        None

def orderbook_ticker(simbolo):
    orderbookticker = client.get_orderbook_ticker(symbol=simbolo)
    return orderbookticker
    #trocar para big order_book com todos os bids e etc, para fazer um algoritimo de henrique aq

def funcaook():
    ok = client.get_account()
    print(ok)

def process_updates(message):
    data = loads(message)
    print(1)
    print(data)
    # last = data["info"]
    # print(last)
    orderlast = {"clientOrderId": data["clientOrderId"]}
    Book[data["clientOrderId"]] = {"info": data["info"],
                                   "last": datetime.now()}
    print(orderlast)

def accuracy_buy(symbol):
    n = Book[symbol]['stepSize'].find('1')
    if n == 0:
        return 0
    elif n > 1:
        return (n - 1)

def accuracy_sell(symbol):
    n = Book[symbol]['tickSize'].find('1')
    if n == 0:
        return 0
    elif n > 1:
        return n - 1

def market_order(symbol,quantity): 
    order = client.order_market_buy(symbol=symbol,quantity=quantity)
    print(order)
# ----------------------------------------------------------------------------------------
def totalsort(list): 
    for i in range(0, len(list)-1): 
        for j in range(0, len(list)-1): 
            if list[j]['total'] > list[j+1]['total']: 
                temp = list[j]
                list[j] = list[j+1]
                list[j+1] = temp
    return list

def totalsort2(list): 
    for i in range(0, len(list)-1): 
        for j in range(0, len(list)-1): 
            if list[j]['totall'] < list[j+1]['totall']: 
                temp = list[j]
                list[j] = list[j+1]
                list[j+1] = temp
    return list

advancedbitcoin = []
primeira = []
soma = 0
max = 0
lucro = []
firstlist = funcao()  

# ----------------------------------------------------------------------------------------
def receiver(list):    
    global primeira

    list['symbol'] = list['symbol'].replace('/','')

    #id == 1 -> começa com bitcoin
    #id == 0 -> termina com bitcoin

    #ordembusd == 1 -> termina com BUSD
    #ordembusd == 0 -> começa com BUSD

    if list['id'] == 1:
        try:
            symbol2 = list['symbol'][3:len(list['symbol'])]
            symbol2do1 = "BUSD" + symbol2 
            total = getBOOKask(symbol2do1)*getBOOKask(list['symbol'])
            primeira.append({'symbol':list['symbol'],'symbolDol':symbol2do1,'total':total,'ordemBUSD': 0,'ordemBTC':0})
        except:
            symbol2 = list['symbol'][3:len(list['symbol'])]
            symbol2do1 = symbol2 + "BUSD"
            total = getBOOKask(symbol2do1)*getBOOKask(list['symbol'])
            primeira.append({'symbol':list['symbol'],'symbolDol':symbol2do1,'total':total,'ordemBUSD': 1,'ordemBTC':0})
    
    else:
        try:
            symbol2 = list['symbol'][0:(len(list['symbol'])-3)]
            symbol2do1 = "BUSD" + symbol2
            total = getBOOKask(symbol2do1)*(1/getBOOKask(list['symbol']))
            primeira.append({'symbol':list['symbol'],'symbolDol':symbol2do1,'total':total,'ordemBUSD': 0,'ordemBTC':1})
        except:
            symbol2 = list['symbol'][0:(len(list['symbol'])-3)]
            symbol2do1 =  symbol2 + "BUSD" 
            total = getBOOKask(symbol2do1)*(1/getBOOKask(list['symbol']))
            primeira.append({'symbol':list['symbol'],'symbolDol':symbol2do1,'total':total,'ordemBUSD': 1,'ordemBTC':1})

    funcao2(primeira)
# ----------------------------------------------------------------------------------------
def funcao2(advancedbitcoin1):
    global lucro
    global primeira
    advancedbitcoin1 = totalsort(advancedbitcoin1)
    print(len(advancedbitcoin1))

    if len(advancedbitcoin1) > 200: 
        primeira = []
    
    if len(advancedbitcoin1) > 100:
        for i in range(0, len(advancedbitcoin1)):
         for j in range(0, len(advancedbitcoin1)): 
                if advancedbitcoin1[i]['ordemBUSD'] == 0:
                    first_amount = 100 * float(getBOOKask(advancedbitcoin1[i]['symbolDol'])) * 0.999
                elif advancedbitcoin1[i]['ordemBUSD'] == 1:
                    first_amount = 100 * 0.999 / float(getBOOKask(advancedbitcoin1[i]['symbolDol'])) 

                if advancedbitcoin1[i]['ordemBTC'] == 0:
                    second_amount = first_amount / getBOOKask(advancedbitcoin1[i]['symbol'])
                elif advancedbitcoin1[i]['ordemBTC'] == 1:
                    second_amount = first_amount * getBOOKask(advancedbitcoin1[i]['symbol'])
    
                if advancedbitcoin1[j]['ordemBTC'] == 0:
                    third_amount = second_amount * getBOOKask(advancedbitcoin1[j]['symbol'])
                elif advancedbitcoin1[j]['ordemBTC'] == 1:
                    third_amount = second_amount / getBOOKask(advancedbitcoin1[j]['symbol'])
    
                if advancedbitcoin1[j]['ordemBUSD'] == 0:
                    fourth_amount = third_amount * 0.999/ getBOOKask(advancedbitcoin1[j]['symbolDol'])
                elif advancedbitcoin1[j]['ordemBUSD'] == 1:
                    fourth_amount = third_amount * getBOOKask(advancedbitcoin1[j]['symbolDol']) * 0.999
            
                if fourth_amount > 100:
                    lucro.append({'symboldol1': advancedbitcoin1[i]['symbolDol'],'symbol1': advancedbitcoin1[i]['symbol'],'symbol2': advancedbitcoin1[j]['symbol'], 'symboldol2': advancedbitcoin1[j]['symbolDol'], 'totall': fourth_amount,
                'primeira_quantidade': first_amount, 'segunda_quantidade': second_amount, 'terceira_quantidade': third_amount, 'quarta_quantidade': fourth_amount
                ,'ordemBUSD1': advancedbitcoin1[i]['ordemBUSD'],'ordemBUSD2':advancedbitcoin1[j]['ordemBUSD'],
                'ordemBTC1':advancedbitcoin1[i]['ordemBTC'],'ordemBTC2': advancedbitcoin1[j]['ordemBTC']})

    if totalsort2(lucro)[0]['totall'] > 100:
        print(totalsort2(lucro)[0])
        executa(totalsort2(lucro))
    print("--------------------------------------")

    lucro = []
# ----------------------------------------------------------------------------------------
maximo = 0
def executa(list): 
    global maximo
    global soma 
    tem = False
    for i in range(0, len(list)):
        first_qty = float(orderbook_ticker(list[i]['symboldol1'])['askPrice']) * float(orderbook_ticker(list[i]['symboldol1'])['askQty'])
        second_qty = float(orderbook_ticker(list[i]['symbol1'])['askPrice']) * float(orderbook_ticker(list[i]['symbol1'])['askQty']) * getBOOKask("BTCBUSD") 
        third_qty = float(orderbook_ticker(list[i]['symboldol2'])['askPrice']) * float(orderbook_ticker(list[i]['symboldol2'])['askQty']) #
        fourth_qty = float(orderbook_ticker(list[i]['symbol2'])['askPrice']) * float(orderbook_ticker(list[i]['symbol2'])['askQty']) * getBOOKask("BTCBUSD")
        
        minimo = min(first_qty,min(second_qty,min(third_qty,fourth_qty)))   
        if ('MARKET' in (get_symbol_info(list[i]['symboldol1']))):
            pode1 = True
        if ('MARKET' in (get_symbol_info(list[i]['symbol1']))):
            pode2 = True         
        if ('MARKET' in (get_symbol_info(list[i]['symbol2']))):
            pode3 = True    
        if ('MARKET' in (get_symbol_info(list[i]['symboldol2']))):
            pode4 = True
        pode = pode1 and (pode2 and (pode3 and pode4))

        if minimo > 20: 
            parou = i
            tem = True
            break
    
    if tem == True:

        if list[parou]['ordemBUSD1'] == 1: #termina com busd
            primeira_quantidade = 100000 / (float(orderbook_ticker(list[parou]['symboldol1'])['askPrice']))
        else: 
            primeira_quantidade = 100000 * (float(orderbook_ticker(list[parou]['symboldol1'])['askPrice']))

        if list[parou]['ordemBTC1'] == 1: #comeca com bitcoin
            segunda_quantidade =  primeira_quantidade * (float(orderbook_ticker(list[parou]['symbol1'])['askPrice']))
        else: 
            segunda_quantidade =  primeira_quantidade / (float(orderbook_ticker(list[parou]['symbol1'])['askPrice']))

        if list[parou]['ordemBTC2'] == 1: #comeca com bitcoin
            terceira_quantidade =  segunda_quantidade / (float(orderbook_ticker(list[parou]['symbol2'])['askPrice']))
        else: 
            terceira_quantidade =  segunda_quantidade * (float(orderbook_ticker(list[parou]['symbol2'])['askPrice']))
        
        if list[parou]['ordemBUSD2'] == 1: #termina com busd
            quarta_quantidade = terceira_quantidade * (float(orderbook_ticker(list[parou]['symboldol2'])['askPrice']))
        else: 
            quarta_quantidade = terceira_quantidade / (float(orderbook_ticker(list[parou]['symboldol2'])['askPrice']))
    
    primeiraprecisao = get_symbol_infothers(list[parou]['symboldol1'])['baseAssetPrecision']
    segundaprecisao = get_symbol_infothers(list[parou]['symbol1'])['baseAssetPrecision']
    terceiraprecisao = get_symbol_infothers(list[parou]['symbol2'])['baseAssetPrecision']
    quartaprecisao = get_symbol_infothers(list[parou]['symboldol2'])['baseAssetPrecision']

    primeira_quantidadeStepSize = float(get_symbol_infothers(list[parou]['symbol1'])['filters'][2]['stepSize'])
    segunda_quantidadeStepSize = float(get_symbol_infothers(list[parou]['symbol1'])['filters'][2]['stepSize'])
    terceira_quantidadeStepSize = float(get_symbol_infothers(list[parou]['symbol2'])['filters'][2]['stepSize'])
    quarta_quantidadeStepSize = float(get_symbol_infothers(list[parou]['symboldol2'])['filters'][2]['stepSize'])

    falta1 = (primeira_quantidade % primeira_quantidadeStepSize)
    primeira_quantidade -= falta1
    primeira_quantidade = "{:0.0{}f}".format(primeira_quantidade, primeiraprecisao)

    falta2 = (segunda_quantidade % segunda_quantidadeStepSize)
    segunda_quantidade -= falta2
    segunda_quantidade = "{:0.0{}f}".format(segunda_quantidade, segundaprecisao)

    falta3 = (terceira_quantidade % terceira_quantidadeStepSize)
    terceira_quantidade -= falta3
    terceira_quantidade = "{:0.0{}f}".format(terceira_quantidade, terceiraprecisao)

    falta4 = (quarta_quantidade % quarta_quantidadeStepSize)
    quarta_quantidade -= falta4
    quarta_quantidade = "{:0.0{}f}".format(quarta_quantidade, quartaprecisao)

    print(primeira_quantidade)
    print(segunda_quantidade)
    print(terceira_quantidade)
    print(quarta_quantidade)

    if minimo > maximo:
        maximo = minimo 
    total = (100000 * (float(list[parou]['totall'])-100))/100
    soma += total
    print(f"o minimo é:{minimo}")
    print(total)
    print(soma) 
    print(f'O máximo é:{maximo}')

# #---------------------------------------------------------------------
#     print("mandei ordem")

#     print(list[parou]['symboldol1'])

#     if list[parou]['ordemBUSD1'] == 1: # 1 -> termina com BUSD
#         mainbuy(primeira_quantidade,list[parou]['symboldol1'])
#         segunda_quantidade = float(assetbalance(list[parou]['symboldol1'][0:len(list[parou]['symboldol1'])-4])['free'])
#     else: 
#         mainsell(primeira_quantidade,list[parou]['symboldol1'])
#         segunda_quantidade = float(assetbalance(list[parou]['symboldol1'][4:len(list[parou]['symboldol1'])])['free'])
# #-------------------------------------------
#     print(segunda_quantidade)
#     if list[parou]['ordemBTC1'] == 1: #comeca com bitcoin
#         segunda_quantidade = segunda_quantidade * (float(orderbook_ticker(list[parou]['symbol1'])['askPrice']))
#     else: #termina com bitcoin
#         segunda_quantidade = segunda_quantidade / (float(orderbook_ticker(list[parou]['symbol1'])['askPrice']))
#     print(segunda_quantidade)
#     falta2 = (segunda_quantidade % segunda_quantidadeStepSize)
#     segunda_quantidade -= falta2
#     segunda_quantidade = "{:0.0{}f}".format(segunda_quantidade, segundaprecisao)
#     print(segunda_quantidade)
#     if list[parou]['ordemBTC1'] == 1: 
#         mainbuy(segunda_quantidade, list[parou]['symbol1'])
#         terceira_quantidade = float(assetbalance('BTC')['free'])
#     else: 
#         mainsell(segunda_quantidade, list[parou]['symbol1'])
#         terceira_quantidade = float(assetbalance('BTC')['free'])
# #-------------------------------------------
#     if list[parou]['ordemBTC2'] == 1: 
#         terceira_quantidade = terceira_quantidade * (float(orderbook_ticker(list[parou]['symbol2'])['askPrice']))
#     else: 
#         terceira_quantidade = terceira_quantidade / (float(orderbook_ticker(list[parou]['symbol2'])['askPrice']))

#     terceira_quantidade = float(terceira_quantidade)
#     falta3 = (terceira_quantidade % terceira_quantidadeStepSize)
#     terceira_quantidade -= falta3
#     terceira_quantidade = "{:0.0{}f}".format(terceira_quantidade, terceiraprecisao)

#     if list[parou]['ordemBTC2'] == 1: 
#         mainsell(terceira_quantidade,list[parou]['symbol2'])
#         quarta_quantidade = float(assetbalance(list[parou]['symbol2'][4:len(list[parou]['symbol2'])])['free'])
#     else: 
#         mainbuy(terceira_quantidade,list[parou]['symbol2'])
#         quarta_quantidade = float(assetbalance(list[parou]['symbol2'][0:len(list[parou]['symbol2'])])['free'])
# #-------------------------------------------
#     if list[parou]['ordemBUSD2'] == 1: #termina com busd
#         quarta_quantidade = quarta_quantidade / (float(orderbook_ticker(list[parou]['symboldol2'])['askPrice']))
#     else: 
#         quarta_quantidade = quarta_quantidade * (float(orderbook_ticker(list[parou]['symboldol2'])['askPrice']))

#     quarta_quantidade = float(quarta_quantidade)
#     falta4 = (quarta_quantidade % quarta_quantidadeStepSize)
#     quarta_quantidade -= falta4
#     quarta_quantidade = "{:0.0{}f}".format(quarta_quantidade, quartaprecisao)

#     if list[parou]['ordemBUSD2'] == 1: 
#         mainbuy(quarta_quantidade,list[parou]['symboldol2'])
#     else: 
#         mainsell(quarta_quantidade,list[parou]['symboldol2'])
# #---------------------------------------------------------------------
#     print(list[parou]['symboldol1'])
#     print(get_symbol_infothers(list[parou]['symboldol1']))
#     mainbuy(primeira_quantidade,list[parou]['symboldol1'])


    #market_buy(list[parou]['symboldol1'],primeira_quantidade)
    # time.sleep(1.0)
    # market_buy(list[parou]['symbol1'],segunda_quantidade)
    # time.sleep(1.0)
    # market_buy(list[parou]['symbol2'],terceira_quantidade)
    # time.sleep(1.0)
    # market_buy(list[parou]['symboldol2'],quarta_quantidade)
    # time.sleep(1.0) 

# ----------------------------------------------------------------------------------------
def run(orderbooks, update, orderexec, symbolfilter, lock):
    current_time = datetime.now()
    while True:
        # print(boleano)
        for x in firstlist:
            try:
                # print(combinations)
                # profit_combinations(combinations)
                #   # erro do except print,
                receiver(x)
                current_time = update['last_update']
                time.sleep(1.0)
            except Exception:
                continue
# ----------------------------------------------------------------------------------------
if __name__ == "__main__":
    # data management
    lock = threading.Lock()
    orderbooks = {}
    orderexec = {}
    orderlast = {}
    ordercancel = {}
    symbolfilter = []
    update = {
        "last_update": None,
    }
    # create websocket threads
    # filter = Filter(
    #     Vmin= 0,
    #     coin=["BUSD","USDT","USDC"],
    #     exchange="Filter",
    #     orderbook=symbolfilter,
    #     lock=lock,
    #     main=main
    # )
    chain = Chain(
        url="wss://stream.binance.com:9443/ws/!bookTicker",
        orderbook=orderbooks,
        lock=lock
    )
    orders = Order(
        url="wss://stream.binance.com:9443",
        orderbook=orderexec,
        lock=lock
    )
    # start threads
    chain.start()
    # time.sleep(10)
    orders.start()
    time.sleep(1)
    # thread.start_new_thread(binance, ())
    run(orderbooks, update, orderexec, symbolfilter, lock)