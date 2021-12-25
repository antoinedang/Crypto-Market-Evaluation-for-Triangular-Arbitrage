from os import times
from typing import final
import ccxt
from ccxt.base import exchange
from ccxt.bitbank import bitbank
from ccxt.bitbns import bitbns
from ccxt.bitfinex import bitfinex
from ccxt.btcalpha import btcalpha
from ccxt.eqonex import eqonex
from ccxt.ftxus import ftxus
from ccxt.okcoin import okcoin
import numpy as np
import math
import time
from datetime import datetime


currencies = ['ETH', 'BTC', 'ADA', 'XLM', 'XMR', 'SOL', 'LTC', 'USDK', 'DAI', 'USDC', 'USDT', 'AVAX', 'BNB', 'XRP', 'DOT', 'BCH', 'USD', 'UST', 'MATIC', 'SHIB', 'DOGE', 'LINK', 'BIX'] #currencies we care about
quote_currencies = ['ETH', 'BTC', 'USDT', 'USDC', 'USDK', 'DAI', 'USD', 'UST'] #quote currencies
stable_currencies = ['USDT', 'USD'] #all conversions start and end in these currencies (what we can trade with)
currency_pairs = [ x + '/'+ y for x in currencies for y in quote_currencies if x != y ]
min_margin_percent = 0.05 #0.05% percent profit at least
max_margin_percent = 50 #anything above 50% profit isnt realistic and shouldn't be acted upon
useAllExchangeCurrencies = False #uses all available currency pairs that have a quote currency in our quote currencies list

inf = 9999999
lastLog = time.time()

okex = ccxt.okex({
    #'apiKey': '64fbbcba-ac0a-4f03-9cd9-c63218e7226b',
    #'secret': '5C3E4309FD39552E6470FB649E0D3D71',
    #'password': 'Ilove2flyH1gh'
    #'enableRateLimit': True,
})
binanceus = ccxt.binanceus()
idex = ccxt.idex()
itbit = ccxt.itbit()
ndax = ccxt.ndax()
eqonex = ccxt.eqonex()
poloniex = ccxt.poloniex()
bitmart = ccxt.bitmart()
bittrex = ccxt.bittrex()
gemini = ccxt.gemini()
kraken = ccxt.kraken()
bibox = ccxt.bibox()
ftxus = ccxt.ftxus()
btcalpha = ccxt.btcalpha()
bitflyer = ccxt.bitflyer()
kucoin = ccxt.kucoin()
gateio = ccxt.gateio()
aax = ccxt.aax()
bequant = ccxt.bequant()
bigone = ccxt.bigone()
bitbank = ccxt.bitbank()
bitbns = ccxt.bitbns()
bitfinex = ccxt.bitfinex()

#, bittrex:0.0035, kraken:0.0026, gemini:0.0035, kucoin:0.001

exchanges = { bibox:0.002, bitfinex:0.002, bitbns:0.0025, bitbank:0.0012, bigone:0.002, bequant:0.001, aax:0.001, gateio:0.002, bitflyer:0.001, okex:0.001, binanceus:0.001, eqonex:0.0009, bitmart:0.0025, ftxus:0.004, itbit:0.0035, idex:0.0025, poloniex:0.00155, btcalpha:0.002 }
# { exchange_name : transaction_fee, name : fee, .... }


#always start and end conversions with USDT (so our portfolio does not depend on crypto markets but rather their imprecisions)
def findOppurtunity(conversion_rates):

    oppurtunities = []

    V = len(conversion_rates.keys())

    for startVertex in stable_currencies:
        if startVertex in conversion_rates.keys():
            distance = {}
            previous = {}
            hasCycle = False

            #initialize empty distance dictionary
            for vertex in conversion_rates.keys():
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
                        previous[end] = start
                        hasCycle = True
                        lastEditedVertex = start
                        break

            if hasCycle:
                conversion_path = {}
                vert = lastEditedVertex
                while vert not in conversion_path.keys():
                    conversion_path[vert] = previous[vert]
                    vert = previous[vert]

                conversion_path['stable'] = startVertex
                oppurtunities.append(conversion_path)

    return oppurtunities


def loadConversionRates(exchange, transactionFee):
    exchange.load_markets()
    log("MARKETS LOADED", False, True)
    conversion_rates = {}

    global currency_pairs

    if useAllExchangeCurrencies:
        currency_pairs = exchange.symbols

    for pair in currency_pairs:
        if pair in exchange.symbols and pair.split("/")[1] in quote_currencies:
            orderbook = exchange.fetch_order_book (pair)
            #BTC/USD
            #bid = best price (USD) you can sell 1 BTC at
            #ask = best price (USD) you can buy 1 BTC at
            bid = orderbook['bids'][0][0] if len (orderbook['bids']) > 0 else None
            ask = orderbook['asks'][0][0] if len (orderbook['asks']) > 0 else None

            cur1 = pair.split("/")[0]
            cur2 = pair.split("/")[1]

            if bid == None or ask == None: continue

            print("        " + exchange.id, { 'pair': pair, 'highest bid': bid, 'lowest ask': ask })

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

    log = open("logs/"+filename, 'a+')
    print(text + timeString)
    log.write("\n" + text + timeString)
    log.close()
    lastLog = time.time()

def exploreOppurtunities(oppurtunities, conversion_rates):
    for oppurtunity in oppurtunities:
        log("!! FOUND OPPURTUNITY: " + str(oppurtunity), False, False)
        value = 1.0
        stableCurrency = oppurtunity.pop('stable', stable_currencies[0])
        startingCurrency = list(oppurtunity.values())[len(list(oppurtunity.values())) - 1]
        finalCurrency = list(oppurtunity.keys())[0]

        #make sure we start from a stable currency
        if (startingCurrency not in stable_currencies):
            log(" > " + str(value) + " " + stableCurrency + " converts to: " + str(value*math.exp(-1*conversion_rates[stableCurrency][startingCurrency])) + " " + startingCurrency, False, False)
            value = value*math.exp(-1*conversion_rates[stableCurrency][startingCurrency])
            startingCurrency = stableCurrency

        previousStartCurr = None
        #do each conversion in the oppurtunity
        for endCurr, startCurr in reversed(oppurtunity.items()):
            if (startCurr != stableCurrency or previousStartCurr == None):
                previousStartCurr = startCurr
                log(" 1> " + str(value) + " " + startCurr + " converts to: " + str(value*math.exp(-1*conversion_rates[startCurr][endCurr])) + " " + endCurr, False, False)
                value = value*math.exp(-1*conversion_rates[startCurr][endCurr])

        #check if there is one more conversion we need
        if ( startingCurrency != finalCurrency ): 
            log(" 2> " + str(value) + " " + finalCurrency + " converts to: " + str(value*math.exp(-1*conversion_rates[finalCurrency][startingCurrency])) + " " + startingCurrency, False, False)
            value = value*math.exp(-1*conversion_rates[finalCurrency][startingCurrency])
            finalCurrency = startingCurrency
        
        #make sure we end up with a stable currency
        if (finalCurrency not in stable_currencies):
            log(" 3> " + str(value) + " " + finalCurrency + " converts to: " + str(value*math.exp(-1*conversion_rates[finalCurrency][stableCurrency])) + " " + stableCurrency, False, False)
            value = value*math.exp(-1*conversion_rates[finalCurrency][stableCurrency])
            finalCurrency = stableCurrency    

        growth = (value-1.0)*100
        log("So we can go from 1.0 " + startingCurrency + " to " + str(value) + " " + finalCurrency + ", an increase of " + str(growth) + "%", False, True)
        if growth >= min_margin_percent and growth < max_margin_percent:
            doTransactions(oppurtunity)
            return True
        else:
            return False


def doTransactions(oppurtunity):
    # do the actual money moving here
    return

def search():
    while True:
        for exchange, transactionFee in exchanges.items():
            log("\n" + exchange.id, False, True)
            try:
                conversion_rates = loadConversionRates(exchange, transactionFee)
                log("CONVERSION RATES LOADED (" + str(len(conversion_rates.keys())) + ")", True, False)
                oppurtunities = findOppurtunity(conversion_rates)
                if len(oppurtunities) == 0:
                    log("NO ARBITRAGE OPPURTUNITIES :(", False, False)
                else:
                    if (exploreOppurtunities(oppurtunities, conversion_rates)): keepExploitingOppurtunity(exchange, transactionFee)
            except Exception as e:
                log("  >  ERROR: " + str(e), False, False)

def keepExploitingOppurtunity(exchange, transactionFee):
    while True:
        try:
            log("\n" + exchange.id, False, True)
            conversion_rates = loadConversionRates(exchange, transactionFee)
            log("CONVERSION RATES LOADED (" + str(len(conversion_rates.keys())) + ")", True, False)
            oppurtunities = findOppurtunity(conversion_rates)
            if len(oppurtunities) == 0:
                return
            else:
                if(not exploreOppurtunities(oppurtunities, conversion_rates)): return
        except Exception as e:
            log("  >  ERROR: " + str(e), False, False)
            return

############################################
############################################

if __name__ == "__main__": search()