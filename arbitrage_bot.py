import ccxt
from ccxt.bitfinex import bitfinex
from ccxt.bitfinex2 import bitfinex2
from ccxt.bitflyer import bitflyer
from ccxt.bitforex import bitforex
from ccxt.digifinex import digifinex
from ccxt.eqonex import eqonex
from ccxt.flowbtc import flowbtc
from ccxt.ftxus import ftxus
from ccxt.hitbtc3 import hitbtc3
from ccxt.hollaex import hollaex
from ccxt.huobijp import huobijp
from ccxt.independentreserve import independentreserve
from ccxt.indodax import indodax
from ccxt.itbit import itbit
from ccxt.kucoin import kucoin
from ccxt.latoken import latoken
from ccxt.latoken1 import latoken1
from ccxt.lbank import lbank
from ccxt.mercado import mercado
from ccxt.novadax import novadax
from ccxt.oceanex import oceanex
from ccxt.okcoin import okcoin
from ccxt.okex3 import okex3
from ccxt.okex5 import okex5
from ccxt.paymium import paymium
from ccxt.poloniex import poloniex
from ccxt.probit import probit
from ccxt.ripio import ripio
from ccxt.stex import stex
from ccxt.therock import therock
from ccxt.tidebit import tidebit
from ccxt.timex import timex
from ccxt.whitebit import whitebit
from ccxt.xena import xena
from ccxt.zipmex import zipmex
import numpy as np
import math
import time
from datetime import datetime
import copy

from numpy.core.numeric import count_nonzero

currencies = ['ETH', 'BTC', 'ADA', 'XLM', 'XMR', 'SOL', 'LTC', 'USDK', 'DAI', 'USDC', 'USDT', 'AVAX', 'BNB', 'XRP', 'DOT', 'BCH', 'USD', 'UST', 'MATIC', 'SHIB', 'DOGE', 'LINK', 'BIX', 'TRX', 'SAND', 'BAC', 'JWL', 'WEC', 'AAVE', 'ZEC', '1INCH', 'GERA', 'REV', 'SPUT', 'EUR'] #currencies we care about
quote_currencies = ['ETH', 'BTC', 'USDT', 'USDC', 'USDK', 'DAI', 'USD', 'UST', 'EUR'] #quote currencies
stable_currencies = ['USDT', 'USD', 'USDC'] #all conversions start and end in these currencies (what we can trade with)
maxTransactionSizeCurrency = 'USD'
currency_pairs = [ x + '/'+ y for x in currencies for y in currencies if x != y ]
min_profit = 0.03 #the conversion must make at least this USD profit to be considered worht it
useAllExchangeCurrencies = False #uses all available currency pairs that have a quote currency in our quote currencies list
useAllExchanges = True #try with every exchange that is offered by ccxt
inf = 9999999
lastLog = time.time()

bigone = ccxt.bigone()
btcalpha = ccxt.btcalpha()
bibox = ccxt.bibox({'password': 'Ilove2flyH1gh'})
binance = ccxt.binance({
    #'apiKey':'CVmVNcQEK9JK3XxoDZq6KGuUmEkvJhhxuTpmyD35SDaey4ASetMEHLaXX4kLZTGk',
    #'secret':'ShmGL7VxeVlDTFjJuOGFGuFf2kHaki8Ub0LM08YINwFtyRIm7pcq9emuXzfgeMEn',
    #'enableRateLimit': True,
    #'options': {'createMarketBuyOrderRequiresPrice': False }
})
binanceus = ccxt.binanceus()
#seed phrase: ripple solid doctor brass rural coyote hour hub pumpkin special canvas action
idex = ccxt.idex({
    'walletAddress':'0x9583d682177b9019b1aed8043bb0e8c36c5ad87a',
    'privateKey': '0xf01eec48610b0cdffde1303c401e7ea87b82cab6a1483cecffea1cc3278fbc30',
    'password':'Ilove2fly',
    'enableRateLimit': True,
    'options': {'createMarketBuyOrderRequiresPrice': False }
})
upbit = ccxt.upbit()

aax = ccxt.aax()
ascendex = ccxt.ascendex()
bequant = ccxt.bequant()
bit2c = ccxt.bit2c()
bitbank = ccxt.bitbank()
bitbns = ccxt.bitbns()
bitcoincom = ccxt.bitcoincom()
bitfinex = ccxt.bitfinex()
bitfinex2 = ccxt.bitfinex2()
bitflyer = ccxt.bitflyer()
bitforex = ccxt.bitforex()
bitget = ccxt.bitget()
bithumb = ccxt.bithumb()
bitmart = ccxt.bitmart()
bitmex = ccxt.bitmex()
bitpanda = ccxt.bitpanda()
bitrue = ccxt.bitrue()
bitso = ccxt.bitso()
bitstamp = ccxt.bitstamp()
bitstamp1 = ccxt.bitstamp1()
bittrex = ccxt.bittrex()
bitvavo = ccxt.bitvavo()
bl3p = ccxt.bl3p()
btcbox = ccxt.btcbox()
btcmarkets = ccxt.btcmarkets()
btctradeua = ccxt.btctradeua()
btcturk = ccxt.btcturk()
buda = ccxt.buda()
bw = ccxt.bw()
bybit = ccxt.bybit()
bytetrade = ccxt.bytetrade()
cdax = ccxt.cdax()
cex = ccxt.cex()
coinbasepro = ccxt.coinbasepro()
coincheck = ccxt.coincheck()
coinex = ccxt.coinex()
coinfalcon = ccxt.coinfalcon()
coinmate = ccxt.coinmate()
coinone = ccxt.coinone()
coinspot = ccxt.coinspot()
crex24 = ccxt.crex24()
currencycom = ccxt.currencycom()
delta = ccxt.delta()
deribit = ccxt.deribit()
digifinex = ccxt.digifinex()
eqonex = ccxt.eqonex()
equos = ccxt.equos()
exmo = ccxt.exmo()
flowbtc = ccxt.flowbtc()
ftx = ccxt.ftx()
ftxus = ccxt.ftxus()
gateio = ccxt.gateio()
gemini = ccxt.gemini()
hitbtc = ccxt.hitbtc()
hitbtc3 = ccxt.hitbtc3()
hollaex = ccxt.hollaex()
huobi = ccxt.huobi()
huobijp = ccxt.huobijp()
independentreserve = ccxt.independentreserve()
indodax = ccxt.indodax()
itbit = ccxt.itbit()
kraken = ccxt.kraken()
kucoin = ccxt.kucoin()
kuna = ccxt.kuna()
latoken = ccxt.latoken()
latoken1 = ccxt.latoken1()
lbank = ccxt.lbank()
liquid = ccxt.liquid()
luno = ccxt.luno()
lykke = ccxt.lykke()
mercado = ccxt.mercado()
mexc = ccxt.mexc()
ndax = ccxt.ndax()
novadax = ccxt.novadax()
oceanex = ccxt.oceanex()
okcoin = ccxt.okcoin()
okex = ccxt.okex()
okex3 = ccxt.okex3()
okex5 = ccxt.okex5()
paymium = ccxt.paymium()
phemex = ccxt.phemex()
poloniex = ccxt.poloniex()
probit = ccxt.probit()
qtrade = ccxt.qtrade()
ripio = ccxt.ripio()
stex = ccxt.stex()
therock = ccxt.therock()
tidebit = ccxt.tidebit()
tidex = ccxt.tidex()
timex = ccxt.timex()
vcc = ccxt.vcc()
wavesexchange = ccxt.wavesexchange()
whitebit = ccxt.whitebit()
xena = ccxt.xena()
yobit = ccxt.yobit()
zaif = ccxt.zaif()
zb = ccxt.zb()
zipmex = ccxt.zipmex()
zonda = ccxt.zonda()


test_exchanges = { lykke:0.0, aax:0.001, ascendex:0.002, bequant:0.001, bitbank:0.0015, bitbns:0.0025, bitcoincom:0.0075, bitfinex:0.002, bitfinex2:0.002, bitflyer:0.002, bitforex:0.001, bitget:0.001, bithumb:0.0015, bitmart:0.0025, bitmex:0.0005, bitpanda:0.0015, bitrue:0.0015, bitso:0.001, bitstamp:0.005, bittrex:0.0035, bitvavo:0.0025, bl3p:0.0026, btcmarkets:0.002, btctradeua:0.001, btcturk:0.0009, buda:0.008, bw:0.002, bybit:0.001, cdax:0.002, cex:0.0025, coinbasepro:0.005, coinex:0.002, coinfalcon:0.002, coinmate:0.0035, crex24:0.001, currencycom:0.002, delta:0.0005, digifinex:0.002, eqonex:0.0009, exmo:0.003, flowbtc:0.005, equos:0.0009, ftx:0.0007, ftxus:0.004, gateio:0.002, gemini:0.0035, hitbtc:0.0009, hitbtc3:0.0009, huobi:0.002, huobijp:0.002, independentreserve:0.005, indodax:0.003, itbit:0.0035, kraken:0.015, kucoin:0.001, kuna:0.0025, latoken:0.005, latoken1:0.005, lbank:0.001, liquid:0.0015, luno:0.001, mexc:0.002, ndax:0.002, novadax:0.0025, oceanex:0.001, okcoin:0.0125, okex:0.001, okex3:0.001, okex5:0.001, paymium:0.005, phemex:0.001, poloniex:0.00155, probit:0.002, ripio:0, stex:0.002, therock:0.002, tidebit:0.003, tidex:0.001, timex:0.005, vcc:0.002, whitebit:0.001, xena:0.001, yobit:0.002, zaif:0.002, zb:0.002, zipmex:0.002, zonda:0.0043 }

confirmed_exchanges = { bibox:0.002, binanceus:0.001, upbit:0.002, binance:0.001, bigone:0.002, btcalpha:0.002, idex:0.0025 }

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
            while vert not in conversion_path.values():
                conversion_path[previous[vert]] = vert
                vert = previous[vert]

            conversion_path['stable'] = startVertex
            oppurtunities.append(conversion_path)

    return oppurtunities


def loadConversionRates(exchange, transactionFee):
    markets = exchange.load_markets()
    log("MARKETS LOADED", False, True)
    conversion_rates = {}
    conversion_rates['fee'] = transactionFee
    for stableCurr in stable_currencies:
        conversion_rates[stableCurr] = {stableCurr: np.log(1-transactionFee)*-1 }
    maxSize = {}

    global currency_pairs

    if useAllExchangeCurrencies:
        currency_pairs = markets.keys()

    for pair in currency_pairs:
        if pair in markets.keys():
            try:
                orderbook = exchange.fetch_order_book (pair)
            except Exception as e:
                log("  >   CONVERSION LOADING ERROR")
                continue
            if orderbook == None: continue
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
            except Exception:
                conversion_rates[cur1] = { }
                conversion_rates[cur1][cur2] = np.log(bid*(1-transactionFee)) * -1
          
            try: conversion_rates[cur2][cur1] = np.log((1-transactionFee)/ask) * -1
            except Exception:
                conversion_rates[cur2] = { }
                conversion_rates[cur2][cur1] = np.log((1-transactionFee)/ask) * -1
          
            bidAmount = orderbook['bids'][0][1]
            askAmount = orderbook['asks'][0][1] * ask

            try:
                maxSize[cur1][cur2] = bidAmount #in cur1
            except Exception:
                maxSize[cur1] = {}
                maxSize[cur1][cur2] = bidAmount #in cur1
            try:
                maxSize[cur2][cur1] = askAmount #in cur2
            except Exception:
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

def findStartingCurrency(oppurtunity):
    for key in reversed(list(oppurtunity.keys())):
        if key in stable_currencies: return key
    return None

def exploreOppurtunities(oppurtunities, conversion_rates, exchange, maxSize):
    for oppurtunity in oppurtunities:
        oppurtunityCopy = copy.deepcopy(oppurtunity)
        maxAmount = 999999999
        value = 1.0
        log("FOUND OPPURTUNITY!  >  " + str(oppurtunity), False, False)
        stableCurrency = oppurtunity.pop('stable')
        if stableCurrency not in oppurtunity.keys():
            stableCurrency = findStartingCurrency(oppurtunity)

        currentCurrency = stableCurrency

        #while there are still conversions left, pop the next step and convert
        while(len(oppurtunity.items()) > 0):
            nextCurrency = oppurtunity.pop(currentCurrency, None)
            if nextCurrency == None: break
            log(" > " + str(value) + " " + currentCurrency + " converts to: " + str(value*math.exp(-1*conversion_rates[currentCurrency][nextCurrency])) + " " + nextCurrency, False, False)
            value = value*math.exp(-1*conversion_rates[currentCurrency][nextCurrency])
            if (currentCurrency not in stable_currencies): maxAmount = min(maxAmount, maxSize[currentCurrency][nextCurrency] * math.exp(-1*conversion_rates[currentCurrency][stableCurrency]) / (1-conversion_rates['fee']))
            currentCurrency = nextCurrency

        #make sure we end up with a stable currency
        if (currentCurrency != stableCurrency):
            log(" 1> " + str(value) + " " + currentCurrency + " converts to: " + str(value*math.exp(-1*conversion_rates[currentCurrency][stableCurrency])) + " " + stableCurrency, False, False)
            value = value*math.exp(-1*conversion_rates[currentCurrency][stableCurrency])
            if (currentCurrency not in stable_currencies): maxAmount = min(maxAmount, maxSize[currentCurrency][stableCurrency] * math.exp(-1*conversion_rates[currentCurrency][stableCurrency]) / (1-conversion_rates['fee']))
            currentCurrency = stableCurrency

        growth = (value-1.0)*100
        possible_profit = maxAmount*(value - 1)
        log("So we can go from 1.0 " + stableCurrency + " to " + str(value) + " " + currentCurrency + ", an increase of " + str(growth) + "%", False, True)
        log("We can move "+ str(maxAmount) + " " + stableCurrency + " through this conversion for a final profit of approximately: " + str(possible_profit) + " " + stableCurrency )

        if possible_profit >= min_profit:
            log(exchange.id + "  >  profit of " + possible_profit + " " + stableCurrency, False, True, "profitable_exchanges.txt")
            return doTransactions(oppurtunityCopy, exchange, maxAmount, stableCurrency)
        else:
            return False

def convert(fromCurrency, toCurrency, exchange, conversion_rates, maxSize, stableCurrency):
    try:
        status = None
        if (fromCurrency + "/" + toCurrency) in exchange.symbols:
            maxSize = maxSize / (math.exp(-1*conversion_rates[fromCurrency][stableCurrency]) / (1-conversion_rates['fee']))
            print("MaxSize in " + fromCurrency + ": " + str(maxSize))
            symbol = fromCurrency + "/" + toCurrency
            price = (math.exp(-1*conversion_rates[fromCurrency][toCurrency]) / (1-conversion_rates['fee']) )
            amount = min(exchange.fetch_balance()[fromCurrency]['free'], maxSize)
            print("sell", amount, price)
            status = exchange.create_limit_sell_order(symbol, amount, price, {"timeInForce":"FOK"})
            #turn it into a limit order with a slightly lower price and make it FOK

        elif (toCurrency + "/" + fromCurrency) in exchange.symbols:
            maxSize = maxSize * (math.exp(-1*conversion_rates[stableCurrency][fromCurrency]) / (1-conversion_rates['fee']))
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
        log("  >   " + fromCurrency + " / " + toCurrency + " CONVERSION ERROR: " + str(e))
        return False

def doTransactions(oppurtunity, exchange, maxAmount, stableCurrency):

    oppurtunity['stable'] = stableCurrency

    log(" >>>> EXPLOITING OPPURTUNITY!  >  " + str(oppurtunity), False, False)
    
    #print initial account balance
    startingBalance = exchange.fetch_balance()[stableCurrency]['free']
    log(" >>>> INITIAL BALANCE: " + startingBalance + " " + stableCurrency)

    stableCurrency = oppurtunity.pop('stable')
    currentCurrency = stableCurrency

    #while there are still conversions left, pop the next step and convert
    while(len(oppurtunity.items()) > 0):
        nextCurrency = oppurtunity.pop(currentCurrency, None)
        if nextCurrency == None: break
        success = convert(currentCurrency, nextCurrency, exchange, maxAmount, stableCurrency)
        if not success:
            if currentCurrency != stableCurrency: convert(currentCurrency, stableCurrency, exchange, exchange.fetch_balance()[currentCurrency]['free'], currentCurrency)
            log("  >>>> CONVERSION FAILED FROM " + currentCurrency + " TO " + nextCurrency + ". ABORTING. CURRENT BALANCE AT: " + exchange.fetch_balance()) 
            return False
        else:
            log("  >>>>  BALANCE AFTER " + currentCurrency + " TO " + nextCurrency + ": " + exchange.fetch_balance())
            currentCurrency = nextCurrency

    #make sure we end up with a stable currency
    if (currentCurrency != stableCurrency):
        success = convert(currentCurrency, stableCurrency, exchange, exchange.fetch_balance()[currentCurrency]['free'], currentCurrency)
        if not success:
            convert(currentCurrency, stableCurrency, exchange, exchange.fetch_balance()[currentCurrency]['free'], currentCurrency)
            log("  >>>> CONVERSION FAILED FROM " + currentCurrency + " TO " + stableCurrency + ". ABORTING. CURRENT BALANCE AT: " + exchange.fetch_balance()) 
            return False
        log("  >>>>  BALANCE AFTER " + currentCurrency + " TO " + stableCurrency + ": " + exchange.fetch_balance())
        currentCurrency = stableCurrency
    
    #print final account balance
    final_balance = exchange.fetch_balance()[stableCurrency]['free']
    log(" >>>> FINAL BALANCE: " + final_balance + " " + stableCurrency, False, True)
    if final_balance > startingBalance: return True
    else: return False

def search():
    while True:
        for exchange, transactionFee in list(test_exchanges.items()) + list(confirmed_exchanges.items()):
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
                log("  >   SEARCH ERROR: " + str(e))

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
            log("  >   KEEP EXPLOITING ERROR: " + str(e), False, False)
            return

############################################
############################################

if __name__ == "__main__":
    search()   