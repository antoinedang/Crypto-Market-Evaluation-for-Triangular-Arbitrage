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

from numpy.core.numeric import count_nonzero

currencies = ['ETH', 'BTC', 'ADA', 'XLM', 'XMR', 'SOL', 'LTC', 'USDK', 'DAI', 'USDC', 'USDT', 'AVAX', 'BNB', 'XRP', 'DOT', 'BCH', 'USD', 'UST', 'MATIC', 'SHIB', 'DOGE', 'LINK', 'BIX', 'TRX', 'SAND', 'BAC', 'JWL', 'WEC', 'AAVE', 'ZEC', '1INCH', 'GERA', 'REV', 'SPUT', 'EUR'] #currencies we care about
quote_currencies = ['ETH', 'BTC', 'USDT', 'USDC', 'USDK', 'DAI', 'USD', 'UST', 'EUR'] #quote currencies
stable_currencies = ['USDT', 'USDC', 'USD'] #all conversions start and end in these currencies (what we can trade with)
currency_pairs = [ x + '/'+ y for x in currencies for y in quote_currencies if x != y ]
min_margin_percent = 0.05 #0.05% percent profit at least
max_margin_percent = 20 #anything above 20% profit isnt realistic and shouldn't be acted upon
useAllExchangeCurrencies = False #uses all available currency pairs that have a quote currency in our quote currencies list
inf = 9999999
lastLog = time.time()

bigone = ccxt.bigone()
btcalpha = ccxt.btcalpha()
bibox = ccxt.bibox({'password': 'Ilove2flyH1gh'})
binance = ccxt.binance({
    'apiKey':'CVmVNcQEK9JK3XxoDZq6KGuUmEkvJhhxuTpmyD35SDaey4ASetMEHLaXX4kLZTGk',
    'secret':'ShmGL7VxeVlDTFjJuOGFGuFf2kHaki8Ub0LM08YINwFtyRIm7pcq9emuXzfgeMEn',
    'enableRateLimit': True,
    'options': {'createMarketBuyOrderRequiresPrice': False }
})

#seed phrase: ripple solid doctor brass rural coyote hour hub pumpkin special canvas action

idex = ccxt.idex({
    'walletAddress':'0x9583d682177b9019b1aed8043bb0e8c36c5ad87a',
    'privateKey': '0xf01eec48610b0cdffde1303c401e7ea87b82cab6a1483cecffea1cc3278fbc30',
    'password':'Ilove2fly',
    'enableRateLimit': True,
    'options': {'createMarketBuyOrderRequiresPrice': False }
})

exchanges = { binance:0.001, binance:0.001, bibox:0.002, bigone:0.002, btcalpha:0.002, idex:0.0025 }

def findOppurtunity(conversion_rates):

    oppurtunities = []

    V = len(conversion_rates.keys())-1

    for startVertex in stable_currencies:
        if startVertex in conversion_rates.keys():
          distance = {}
          previous = {}
          hasCycle = False

          #initialize empty distance dictionary
          for vertex in conversion_rates.keys():
            if vertex == 'fee': continue
            if startVertex != vertex: distance[vertex] = inf
            else: distance[vertex] = 0.0

          #perform Bellman Ford algorithm V-1 times
          for i in range(V-1):
            for start, ends in conversion_rates.items():
                if start == 'fee': continue
                for end, weight in ends.items():
                    if distance[end] > distance[start] + weight and distance[start] != inf:
                      distance[end] = distance[start] + weight
                      previous[end] = start


          #do Bellman Ford algorithm one more time, this tells us if there is a cycle
          for start, ends in conversion_rates.items():
            if start == 'fee': continue
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
    conversion_rates['fee'] = transactionFee
    conversion_rates['USDT'] = {'USDT': np.log(1-transactionFee)*-1 }
    maxSize = {}

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
          if bid == None or ask == None: continue


          cur1 = pair.split("/")[0]
          cur2 = pair.split("/")[1]

          print("        " + exchange.id, { 'pair': pair, 'highest bid': bid, 'lowest ask': ask, 'maxBidSize':orderbook['bids'][0][1], 'maxAskSize':orderbook['asks'][0][1] })

          try: conversion_rates[cur1][cur2] = np.log(bid*(1-transactionFee)) * -1
          except:
            conversion_rates[cur1] = { }
            conversion_rates[cur1][cur2] = np.log(bid*(1-transactionFee)) * -1
          
          try: conversion_rates[cur2][cur1] = np.log((1-transactionFee)/ask) * -1
          except:
            conversion_rates[cur2] = { }
            conversion_rates[cur2][cur1] = np.log((1-transactionFee)/ask) * -1
          
          bidAmount = orderbook['bids'][0][1]
          askAmount = orderbook['asks'][0][1] * ask

          try:
            maxSize[cur1][cur2] = bidAmount #in cur1
          except:
            maxSize[cur1] = {}
            maxSize[cur1][cur2] = bidAmount #in cur1
          try:
            maxSize[cur2][cur1] = askAmount #in cur2
          except:
            maxSize[cur2] = {} #in cur2
            maxSize[cur2][cur1] = askAmount #in cur2

          
    return conversion_rates, maxSize

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

def exploreOppurtunities(oppurtunities, conversion_rates, exchange, maxSize):
    for oppurtunity in oppurtunities:
        maxUSDT = 999999999
        value = 1.0
        stableCurrency = oppurtunity.pop('stable', stable_currencies[0])
        log("FOUND OPPURTUNITY!  >  " + str(oppurtunity), False, False)
        startingCurrency = list(oppurtunity.values())[len(list(oppurtunity.values())) - 1]
        finalCurrency = list(oppurtunity.keys())[0]


        #check if one of the steps has USDT as its key and make sure it is first in the dictionary


        #make sure we start from a stable currency
        if (startingCurrency not in stable_currencies):
            log(" 1> " + str(value) + " " + stableCurrency + " converts to: " + str(value*math.exp(-1*conversion_rates[stableCurrency][startingCurrency])) + " " + startingCurrency, False, False)
            value = value*math.exp(-1*conversion_rates[stableCurrency][startingCurrency])
            maxUSDT = min(maxUSDT, maxSize[stableCurrency][startingCurrency] * math.exp(-1*conversion_rates[stableCurrency]['USDT']) / (1-conversion_rates['fee']))
            startingCurrency = stableCurrency

        previousStartCurr = None
        #do each conversion in the oppurtunity
        for endCurr, startCurr in reversed(oppurtunity.items()):
            if (startCurr != stableCurrency or previousStartCurr == None):
                previousStartCurr = startCurr
                log(" 2> " + str(value) + " " + startCurr + " converts to: " + str(value*math.exp(-1*conversion_rates[startCurr][endCurr])) + " " + endCurr, False, False)
                value = value*math.exp(-1*conversion_rates[startCurr][endCurr])
                maxUSDT = min(maxUSDT, maxSize[startCurr][endCurr]*math.exp(-1*conversion_rates[startCurr]['USDT'] / (1-conversion_rates['fee'])))
        
        #make sure we end up with a stable currency
        if (finalCurrency not in stable_currencies):
            log(" 3> " + str(value) + " " + finalCurrency + " converts to: " + str(value*math.exp(-1*conversion_rates[finalCurrency][stableCurrency])) + " " + stableCurrency, False, False)
            value = value*math.exp(-1*conversion_rates[finalCurrency][stableCurrency])
            maxUSDT = min(maxUSDT, maxSize[finalCurrency][stableCurrency] * math.exp(-1*conversion_rates[finalCurrency]['USDT']) / (1-conversion_rates['fee']))
            finalCurrency = stableCurrency    

        growth = (value-1.0)*100
        log("So we can go from 1.0 " + startingCurrency + " to " + str(value) + " " + finalCurrency + ", an increase of " + str(growth) + "%", False, True)
        log("Maximum USDT we can move through this conversion: " + str(maxUSDT))

        if growth >= min_margin_percent and growth < max_margin_percent:
            doTransactions(oppurtunity, exchange, maxUSDT)
            return True
        else:
            return False

def convert(fromCurrency, toCurrency, exchange, conversion_rates, maxSize=999999999):
    try:
        status = None
        if (fromCurrency + "/" + toCurrency) in exchange.symbols:
            maxSize = maxSize / (math.exp(-1*conversion_rates[fromCurrency]['USDT']) / (1-conversion_rates['fee']))
            print("MaxSize in " + fromCurrency + ": " + str(maxSize))
            symbol = fromCurrency + "/" + toCurrency
            price = (math.exp(-1*conversion_rates[fromCurrency][toCurrency]) / (1-conversion_rates['fee']) )
            amount = min(exchange.fetch_balance()[fromCurrency]['free'], maxSize)
            print("sell", amount, price)
            status = exchange.create_limit_sell_order(symbol, amount, price, {"timeInForce":"FOK"})
            #turn it into a limit order with a slightly lower price and make it FOK

        elif (toCurrency + "/" + fromCurrency) in exchange.symbols:
            maxSize = maxSize * (math.exp(-1*conversion_rates['USDT'][fromCurrency]) / (1-conversion_rates['fee']))
            print("MaxSize in " + fromCurrency + ": " + str(maxSize))
            symbol = toCurrency + "/" + fromCurrency
            price = 1/(math.exp(-1*conversion_rates[fromCurrency][toCurrency]) / (1-conversion_rates['fee']) )
            cost = exchange.fetch_balance()[fromCurrency]['free']
            amount = min(cost/price, maxSize/price)
            print("buy", amount, toCurrency, "for", price, fromCurrency, "a pop")
            status = exchange.create_limit_buy_order(symbol,  amount, price, {"timeInForce":"FOK"})
            #turn it into a limit order with a slightly lower price and make it FOK
        
        print(status)
        return status['status']=="closed"
    except Exception as e:
        log(" > " + fromCurrency + " - " + toCurrency + " CONVERSION ERROR: " + str(e))
        return False

def doTransactions(oppurtunity, exchange, maxUSDT):
    # do the actual money moving here

    #print initial account balance
    log(" >>>> INITIAL BALANCE: " + exchange.fetch_balance())

    stableCurrency = oppurtunity.pop('stable', stable_currencies[0])
    startingCurrency = list(oppurtunity.values())[len(list(oppurtunity.values())) - 1]
    finalCurrency = list(oppurtunity.keys())[0]

    #make sure we start from a stable currency
    if (startingCurrency not in stable_currencies):
        convert(stableCurrency, startingCurrency, exchange, maxUSDT)
        log(" > BALANCE AFTER " + stableCurrency + " TO " + startingCurrency + ": " + exchange.fetch_balance())
        startingCurrency = stableCurrency

    previousStartCurr = None
    #do each conversion in the oppurtunity
    for endCurr, startCurr in reversed(oppurtunity.items()):
        if (startCurr != stableCurrency or previousStartCurr == None):
          if (startCurr == stableCurrency and previousStartCurr == None): convert(startCurr, endCurr, exchange, maxUSDT)
          else: convert(startCurr, endCurr, exchange)
          log(" > BALANCE AFTER " + startCurr + " TO " + endCurr + ": " + exchange.fetch_balance())
          previousStartCurr = startCurr
    
    #make sure we end up with a stable currency
    if (finalCurrency not in stable_currencies):
        convert(finalCurrency, stableCurrency, exchange)
        log(" > BALANCE AFTER " + finalCurrency + " TO " + stableCurrency + ": " + exchange.fetch_balance())
        finalCurrency = stableCurrency

    #print final account balance
    log(" >>>> FINAL BALANCE: " + exchange.fetch_balance(), False, True)

def search():
    while True:
        for exchange, transactionFee in exchanges.items():
          log("\n" + exchange.id, False, True)
          try:
            conversion_rates, maxSize = loadConversionRates(exchange, transactionFee)
            log("CONVERSION RATES LOADED (" + str(len(conversion_rates.keys())) + ")", True, False)
            oppurtunities = findOppurtunity(conversion_rates)
            if len(oppurtunities) == 0:
                log("NO ARBITRAGE OPPURTUNITIES :(", False, False)
            else:
                if (exploreOppurtunities(oppurtunities, conversion_rates, exchange, maxSize)): keepExploitingOppurtunity(exchange, transactionFee)
          except Exception as e:
            log("  >  ERROR: " + str(e), False, False)

def keepExploitingOppurtunity(exchange, transactionFee):
    while True:
        try:
          log("\n" + exchange.id, False, True)
          conversion_rates, maxSize = loadConversionRates(exchange, transactionFee)
          log("CONVERSION RATES LOADED (" + str(len(conversion_rates.keys())) + ")", True, False)
          oppurtunities = findOppurtunity(conversion_rates)
          if len(oppurtunities) == 0:
            log("NO ARBITRAGE OPPURTUNITIES :(", False, False)
            return
          else:
            if(not exploreOppurtunities(oppurtunities, conversion_rates, exchange, maxSize)): return
        except Exception as e:
          log("  >  ERROR: " + str(e), False, False)
          return

############################################
############################################

if __name__ == "__main__":
    #binance.set_sandbox_mode(True) #started with 'BNB': 1000.0, 'BTC': 1.0, 'BUSD': 10000.0, 'ETH': 100.0, 'LTC': 500.0, 'TRX': 500000.0, 'USDT': 10000.0, 'XRP': 50000.0

    search()
    exit()
    fromCurr = 'TRX'
    toCurr = 'USDT'

    conversion_rates, maxSize = loadConversionRates(binance, 0.001)

    print(fromCurr + " BALANCE: " + str(binance.fetch_balance()[fromCurr]['free']))
    print(toCurr + " BALANCE: " + str(binance.fetch_balance()[toCurr]['free']))

    maxTransactionVolume = maxSize[fromCurr][toCurr] * math.exp(-1*conversion_rates[fromCurr]['USDT']) / (1-conversion_rates['fee'])
    print(" > Maximum transaction volume: " + str(maxTransactionVolume))

    print(" > Predicted " + toCurr + " balance after conversion from " + fromCurr + " to " + toCurr + ": " + str(binance.fetch_balance()[toCurr]['free'] + maxTransactionVolume*math.exp(-1*conversion_rates['USDT'][toCurr]) / (1-conversion_rates['fee'])))
    print(" > Predicted " + fromCurr + " balance: " + str(binance.fetch_balance()[fromCurr]['free'] - maxTransactionVolume*(math.exp(-1*conversion_rates['USDT'][fromCurr]) / (1-conversion_rates['fee']))))
    print(convert(fromCurr, toCurr, binance, conversion_rates, maxTransactionVolume))
    print(toCurr + " BALANCE: " + str(binance.fetch_balance()[toCurr]['free']))
    print(fromCurr + " BALANCE: " + str(binance.fetch_balance()[fromCurr]['free']))
   