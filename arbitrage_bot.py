from os import times
import ccxt
from ccxt.eqonex import eqonex
import numpy as np
import math
import time
from datetime import datetime
import threading

inf = 9999999
lastLog = time.time()

triangular_arbitrage_currencies = ['ETH', 'BTC', 'ADA', 'XLM', 'XMR', 'SOL', 'LTC', 'DOGE', 'USDK', 'DAI', 'USDC', 'USDT', 'AVAX', 'BNB', 'XRP', 'DOT', 'BCH']
triangular_arbitrage_stable_currencies = ['USDT'] #all conversions start and end in these currencies
triangular_currency_pairs = [ x + '/'+ y for x in triangular_arbitrage_currencies for y in triangular_arbitrage_currencies if x != y ]
triangular_min_margin = 0.01 #1 percent profit at least (must make at least a cent profit per dollar invested)

#always start and end conversions with USDT (so our portfolio does not depend on crypto markets but rather their imprecisions)
def findTriangularArbitrageOppurtunity(conversion_rates):

    oppurtunities = []

    V = len(triangular_arbitrage_currencies)

    for startVertex in triangular_arbitrage_stable_currencies:
        distance = {}
        previous = {}
        hasCycle = False

        #initialize empty distance dictionary
        for vertex in triangular_arbitrage_currencies:
            if startVertex != vertex: distance[vertex] = inf
            else: distance[vertex] = 0.0

        #perform Bellman Ford algorithm V-1 times
        for i in range(V-1):
            for start, ends in conversion_rates.items():
                for end, weight in ends.items():
                    if distance[end] > distance[start] + weight and distance[start] != inf:
                        distance[end] = distance[start] + weight
                        previous[end] = start
            
        #do Bellman Ford algorithm one more time, this tells us if there is a cycle
        for start, ends in conversion_rates.items():
            for end, weight in ends.items():
                if distance[end] > distance[start] + weight and distance[start] != inf:
                    distance[end] = distance[start] + weight
                    #previous[end] = start
                    hasCycle = True

        if hasCycle:
            conversion_path = {}
            vert = startVertex
            while vert not in conversion_path.keys():
                conversion_path[vert] =  previous[vert]
                vert = previous[vert]

            oppurtunities.append(conversion_path)

    return oppurtunities


def loadConversionRates(exchange, transactionFee):
    exchange.load_markets()
    conversion_rates = {}

    for pair in triangular_currency_pairs:
        if pair in exchange.symbols:
            orderbook = exchange.fetch_order_book (pair)
            #BTC/USD
            #bid = best price (USD) you can sell 1 BTC at
            #ask = best price (USD) you can buy 1 BTC at
            bid = orderbook['bids'][0][0] if len (orderbook['bids']) > 0 else None
            ask = orderbook['asks'][0][0] if len (orderbook['asks']) > 0 else None
            
            cur1 = pair.split("/")[0]
            cur2 = pair.split("/")[1]

            if bid == None or ask == None: continue

            # print(exchange.id, 'market', { 'pair': pair, 'highest bid': bid, 'lowest ask': ask })

            try: conversion_rates[cur1][cur2] = np.log(bid*(1-transactionFee)) * -1
            except:
                conversion_rates[cur1] = { }
                conversion_rates[cur1][cur2] = np.log(bid*(1-transactionFee)) * -1
            
            try: conversion_rates[cur2][cur1] = np.log((1-transactionFee)/ask) * -1
            except:
                conversion_rates[cur2] = { }
                conversion_rates[cur2][cur1] = np.log((1-transactionFee)/ask) * -1
            
    return conversion_rates

def log(text, showTimeElapsed=False, showTime=False, filename="log.txt"):
    global lastLog
    timeString = ""
    if showTime or showTimeElapsed: timeString += "     >     "
    if showTime: timeString += datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    if showTimeElapsed: timeString += " (%.2fs elapsed)" % ((time.time()-lastLog))

    try:
        log = open("logs/"+filename, 'a')
    except:
        log = open("logs/"+filename, 'w')
    print(text + timeString)
    log.write("\n" + text + timeString)
    log.close()
    lastLog = time.time()

def exploreOppurtunities(oppurtunities, conversion_rates):
    for oppurtunity in oppurtunities:
        log("!! FOUND OPPURTUNITY: " + str(oppurtunity), False, False)
        value = 1.0
        startingCurrency = list(oppurtunity.keys())[0]
        finalCurrency = list(oppurtunity.values())[ len(list(oppurtunity.values())) - 1 ]

        for startCurr, endCurr in oppurtunity.items():
            log(" > " + str(value) + " " + startCurr + " converts to: " + str(math.exp(-1*value*conversion_rates[startCurr][endCurr])) + " " + endCurr, False, False)
            value = math.exp(-1*value*conversion_rates[startCurr][endCurr])

        #check if there is one more conversion we need
        if ( startingCurrency != finalCurrency ): 
            log(" > " + str(value) + " " + finalCurrency + " converts to: " + str(math.exp(-1*value*conversion_rates[finalCurrency][startingCurrency])) + " " + startingCurrency, False, False)
            value = math.exp(-1*value*conversion_rates[finalCurrency][startingCurrency])
        
        log("So we can go from 1.0 " + startingCurrency + " to " + str(value) + " " + finalCurrency + ", an increase of " + str((value-1.0)*100) + "%", False, True)
        


############################################
############################################


okex = ccxt.okex({
    #'apiKey': '64fbbcba-ac0a-4f03-9cd9-c63218e7226b',
    #'secret': '5C3E4309FD39552E6470FB649E0D3D71',
    #'password': 'Ilove2flyH1gh'
    #'enableRateLimit': True,
    })

binanceus = ccxt.binanceus()
bibox = ccxt.bibox()
ndax = ccxt.ndax()
kraken = ccxt.kraken()
eqonex = ccxt.eqonex()
poloniex = ccxt.poloniex()

exchanges = { okex:0.001, binanceus:0.001, bibox:0.002, ndax:0.002, kraken:0.0026, eqonex:0.0009, poloniex:0.00155 }

exchanges = { bibox:0.002 }

def run():
    for exchange, transactionFee in exchanges.items():
        log("\n" + exchange.id, False, True)
        # conversion_rates = loadConversionRates(exchange, transactionFee)
        log("CONVERSION RATES LOADED", True, False)
        #print(conversion_rates)
        conversion_rates = {'ETH': {'BTC': 2.518188196327284, 'USDC': -8.314574491825466, 'USDT': -8.315285533898534, 'LTC': -3.225753883493541, 'DOGE': -10.022298170082204, 'XRP': -8.313843449801812, 'BCH': -2.1968474140023146}, 'BTC': {'ETH': -2.5137753206858946, 'USDC': -10.831427675992442, 'USDT': -10.831373420245635, 'LTC': -5.7414281562780145, 'XRP': -10.82984886297388, 'BCH': -4.712617044883851}, 'USDC': {'ETH': 8.319040365542538, 'BTC': 10.83577608734335, 'USDT': 0.016102127049454733}, 'USDT': {'ETH': 8.319291981811956, 'BTC': 10.835379398574805, 'ADA': 0.38138593458008085, 'XLM': -1.249272074773276, 'SOL': 5.248542273607692, 'LTC': 5.0907704901702715, 'DOGE': -1.705379554093554, 'DAI': 0.0018019826680060586, 'USDC': -0.010815501039941298, 'AVAX': 4.810508872667806, 'BNB': 6.3077844674718735, 'XRP': 0.002801682841237318, 'DOT': 3.3783703457701906, 'BCH': 6.120671724013944}, 'ADA': {'USDT': -0.37669467315678035}, 'XLM': {'USDT': 1.2535207455358808}, 'SOL': {'USDT': -5.244253879770787}, 'LTC': {'ETH': 3.2313810437049626, 'BTC': 5.74704719395085, 'USDT': -5.086704826845738}, 'DOGE': {'ETH': 10.027205313890898, 'USDT': 1.7094938555801615}, 'DAI': {'USDT': 0.0026021827427055054}, 'AVAX': {'USDT': -4.806119639502697}, 'BNB': {'USDT': -6.30376220479336}, 'XRP': {'ETH': 8.318992790074269, 'BTC': 10.834865526629612, 'USDT': 0.0012123145564239364}, 'DOT': {'USDT': -3.3740382418596235}, 'BCH': {'ETH': 2.2019249172465867, 'BTC': 4.717824458762359, 'USDT': -6.116425537277549}}
        oppurtunities = findTriangularArbitrageOppurtunity(conversion_rates)
        if len(oppurtunities) == 0: log("NO ARBITRAGE OPPURTUNITIES FOUND", False, False)
        else: exploreOppurtunities(oppurtunities, conversion_rates)
     #run()

run()