import ccxt
import numpy as np
import math
import time
from datetime import datetime
import copy
import traceback
import json


inf = 9999999
quotes = [ 'USDT', 'USDC', 'ETH', 'LTC', 'BIX', 'CHS' ]
currencies = ['USDT', 'USDC', 'ETH', 'LTC', 'ETC', 'EOS', 'BIX', 'QTUM', 'NEO', 'HT', 'BCH', 'ONT', 'XRP', 'ATOM', 'IRIS', 'ALGO', 'OMG', 'BAT', 'KSM', 'BSV', 'TRX', 'AAVE', 'COMP', 'LINK', 'CKB', 'HPB', 'BTM', 'ONG', 'DOGE', 'VNT', 'CHS', 'PLC', 'PHA', 'CRV', 'MKR' ] #currencies we care about
stable_currencies = ['USDT', 'USDC'] #all conversions start and end in these currencies (what we can trade with)
maxCompromises = inf # how many maximum compromises (a compromise is when we take the next best price on the most limiting conversion rather than just the best price)
currency_pairs = [ x + '/'+ y for x in currencies for y in quotes if x != y ]
min_growth = 0.02 # the conversion must yield a profit of at least 0.02%
max_growth = 10 #any growth above 10% is unrealistic and probalby an error
min_profit = 0.01 #the conversion must make at least one cent USD profit to be considered worth it
min_investment = { 'bibox':5 } #we'll only consider transactions we can invest at least this amount of US dollars into
max_investment = { 'bibox':inf } #maximimum transaction size for each exchange
logConversionRates = False
simulateWithTestFunds = True
initialTestFunds ={"bibox":100}
actuallyMakeTransactions = False
lastLog = time.time()
precisionJSON = open('biboxPrecisions.json')
precisionData = json.load(precisionJSON)['result']


bibox = ccxt.bibox({})


bigone = ccxt.bigone()
bitmex = ccxt.bitmex({})
binance = ccxt.binance({
    #'apiKey':'CVmVNcQEK9JK3XxoDZq6KGuUmEkvJhhxuTpmyD35SDaey4ASetMEHLaXX4kLZTGk',
    #'secret':'ShmGL7VxeVlDTFjJuOGFGuFf2kHaki8Ub0LM08YINwFtyRIm7pcq9emuXzfgeMEn',
    #'enableRateLimit': True,
    #'options': {'createMarketBuyOrderRequiresPrice': False }
})
aax = ccxt.aax({'secret':'f7591aa3c2c63c52110cf87cb98a6ed1', 'apiKey':'a0zty4VLfxxqOOQ1gQgnJ9URNo'})
btcalpha = ccxt.btcalpha({'secret':'63hWe1ydFj8L9t6vspZbawYhmmD9WT9xdgy5175XZv8s93SvsNddaMVv6B1irf1mxqknWksEYAhCv7BTQu2pmkJx', 'apiKey':'4poAAqfmJGq3bQEzcWdC9m4wx7bXnLGyuuQyQqgUvikdheAoV8B2orgQiMrVaEA8HAYVc3SDRh92'})
lbank = ccxt.lbank({})
binanceus = ccxt.binanceus()
idex = ccxt.idex()
upbit = ccxt.upbit()
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
kucoin = ccxt.kucoin({'password':'Ilove2fly%percent%', 'secret':'25608af7-631f-4a4f-a0ec-e225f6f3b2e0', 'apiKey':'61cb4d0e895c6300011ef6ae'})
kuna = ccxt.kuna()
latoken = ccxt.latoken()
latoken1 = ccxt.latoken1()
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
wavesexchange = ccxt.wavesexchange()
whitebit = ccxt.whitebit()
xena = ccxt.xena()
yobit = ccxt.yobit()
zaif = ccxt.zaif()
zb = ccxt.zb()
zipmex = ccxt.zipmex()
zonda = ccxt.zonda()


other_exchanges = {  bitmex:0.0005, kucoin:0.001, ascendex:0.002, bequant:0.001, bitbank:0.0015, bitbns:0.0025, bitcoincom:0.0075, bitfinex:0.002, bitfinex2:0.002, bitflyer:0.002, bitforex:0.001, bitget:0.001, bithumb:0.0015, bitmart:0.0025, bitpanda:0.0015, bitso:0.001, bitstamp:0.005, bittrex:0.0035, bitvavo:0.0025, bl3p:0.0026, btcmarkets:0.002, btctradeua:0.001, buda:0.008, bw:0.002, bybit:0.001, cdax:0.002, cex:0.0025, coinbasepro:0.005, coinex:0.002, coinfalcon:0.002, coinmate:0.0035, crex24:0.001, eqonex:0.0009, equos:0.0009, ftx:0.0007, ftxus:0.004, gateio:0.002, huobi:0.002, huobijp:0.002, independentreserve:0.005, indodax:0.003, itbit:0.0035, kraken:0.015, kuna:0.0025, latoken:0.005, latoken1:0.005, liquid:0.0015, luno:0.001, mexc:0.002, ndax:0.002, novadax:0.0025, oceanex:0.001, okcoin:0.0125, okex3:0.001, okex5:0.001, paymium:0.005, phemex:0.001, poloniex:0.00155, probit:0.002, ripio:0, therock:0.002, tidebit:0.003, tidex:0.001, timex:0.005, xena:0.001, zaif:0.002, zb:0.002, zipmex:0.002, zonda:0.0043, lykke:0.0, btcturk:0.0009, btcalpha:0.002, aax:0.001, exmo:0.003, hitbtc3:0.0009, hitbtc:0.0009, whitebit:0.001, yobit:0.002, gemini:0.0035, binanceus:0.001, upbit:0.002, bigone:0.002, idex:0.0025, stex:0.002, okex:0.001, digifinex:0.002, binance:0.001, delta:0.0005, bitrue:0.0015, aax:0.001, btcalpha:0.002, lbank:0.001 }

exchanges = { bibox:0.002 }

def findOppurtunity(conversion_rates, startingVertex=None):

    oppurtunities = []

    V = len(conversion_rates.keys())-1

    if startingVertex != None: starting_currencies = [ startingVertex ]
    else: starting_currencies = stable_currencies

    for startVertex in starting_currencies:
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

def loadConversionRates(exchange, transactionFee, specificConversion=None, compromise_index=0, old_conversion_rates=None, old_max_size=None):
    markets = exchange.load_markets()
    log("MARKETS LOADED", False, True)
    if old_conversion_rates != None:
        conversion_rates = old_conversion_rates
        maxSize = old_max_size
    else:
        conversion_rates = {}
        conversion_rates['fee'] = transactionFee
        for curr in currencies:
            conversion_rates[curr] = {curr: np.log(1-transactionFee)*-1 }
        maxSize = {}
        for curr in currencies:
            maxSize[curr] = { curr:inf }

    global currency_pairs

    for pair in currency_pairs:
        if specificConversion == None or pair == specificConversion:
            if pair in markets.keys():
                try:
                    orderbook = exchange.fetch_order_book (pair)
                except Exception as e:
                    log("  >   CONVERSION LOADING ERROR ")
                    continue

                if orderbook == None: continue


                #BTC/USD
                #bid = best price (USD) you can sell 1 BTC at
                #ask = best price (USD) you can buy 1 BTC at
                index = 0
                maxBidSize = orderbook['bids'][index][1] if len (orderbook['bids']) > index else None
                maxAskSize = orderbook['asks'][index][1] if len (orderbook['asks']) > index else None
                if maxBidSize == None or maxAskSize == None: continue

                if (specificConversion == pair):
                    if len(orderbook['bids']) <= compromise_index or len(orderbook['asks']) <= compromise_index:
                        log("  >   COMPROMISE IMPOSSIBLE. NO BETTER PRICE AVAILABLE.")
                        return None, None
                    try:
                        while(index < compromise_index):
                            index += 1
                            maxBidSize += orderbook['bids'][index][1]
                            maxAskSize += orderbook['asks'][index][1]
                    except Exception as e:
                        log("  >   COMPROMISE FAILED. ABORTING. " + str(traceback.format_exc()))
                        return None, None

                bid = orderbook['bids'][index][0] if len (orderbook['bids']) > index else None
                ask = orderbook['asks'][index][0] if len (orderbook['asks']) > index else None
                if bid == None or ask == None: continue


                cur1 = pair.split("/")[0]
                cur2 = pair.split("/")[1]

                log("        " + ' > pair: ' + pair + ', highest bid: ' + str(bid) + ', lowest ask: ' + str(ask) + ', maxBidSize: ' + str(maxBidSize) + ', maxAskSize: ' + str(maxAskSize), False, False, None, (not logConversionRates) )

                try:
                    conversion_rates[cur1][cur2] = np.log(bid*(1-transactionFee)) * -1
                except Exception:
                    conversion_rates[cur1] = { }
                    conversion_rates[cur1][cur2] = np.log(bid*(1-transactionFee)) * -1
            
                try:
                    conversion_rates[cur2][cur1] = np.log((1-transactionFee)/ask) * -1
                except Exception:
                    conversion_rates[cur2] = { }
                    conversion_rates[cur2][cur1] = np.log((1-transactionFee)/ask) * -1
            
                bidAmount = maxBidSize
                askAmount = maxAskSize * ask

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

def log(text, showTimeElapsed=False, showTime=False, filename="log.txt", justPrint=False):
    global lastLog
    timeString = ""

    if showTime or showTimeElapsed: timeString += "     >     "
    if showTime: timeString += datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    if showTimeElapsed: timeString += " (%.2fs elapsed)" % ((time.time()-lastLog))

    if filename == None: filename = "log.txt"
    print(text + timeString)

    if not justPrint:
        log = open("logs/"+filename, 'a+')
        log.write(text + timeString + "\n")
        log.close()
        if showTime or showTimeElapsed: lastLog = time.time()

def getTestFundsBalance(name):
    try:
        funds = open("test_funds/" + name + ".txt", 'r')
        for line in funds.readlines():
            if line.split(' : ')[0] == 'current': return float(line.split(' : ')[1])
        funds.close()
    except Exception:
        log(" ERROR : Couldn't get test funds balance")
        return None

def updateTestFunds(growthPercent, maxTransaction, name, countAsTrade=True):
    try:
        funds = open("test_funds/" + name + ".txt", 'r')
        for line in funds.readlines():
            if line.split(' : ')[0] == 'startDate': startDate = line.split(' : ')[1].rstrip("\n")
            if line.split(' : ')[0] == 'initial': initial = float(line.split(' : ')[1])
            if line.split(' : ')[0] == 'current': current = float(line.split(' : ')[1])
            if line.split(' : ')[0] == 'numTrades': numTrades = int(line.split(' : ')[1])
            if line.split(' : ')[0] == 'averageGrowthPercent': avgGrowth = float( line.split(' : ')[1].rstrip("%\n") )
        funds.close()
    except Exception:
        startDate = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        initial = initialTestFunds[ name.split("_")[0] ]
        current = initial
        numTrades = 0
        avgGrowth = 0
    
    if countAsTrade:
        sumGrowth = avgGrowth*numTrades + growthPercent
        numTrades += 1
        avgGrowth = sumGrowth/numTrades

    amountToInvest = min(current, maxTransaction)
    current = current + amountToInvest*(growthPercent/100)

    funds = open("test_funds/" + name + ".txt", 'w+')
    funds.write("startDate : " + startDate)
    funds.write("\ninitial : " + str(initial))
    funds.write("\ncurrent : " + str(current))
    funds.write("\nnumTrades : " + str(numTrades))
    funds.write("\naverageGrowthPercent : " + str(avgGrowth) + "%")
    if countAsTrade:
        funds.write("\nlastTradeDate : " + datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))
        start = datetime.strptime(startDate,"%m/%d/%Y, %H:%M:%S")
        now = datetime.now()
        timeElapsed = now-start
        funds.write("\ntimeElapsed : " + str(timeElapsed))
    else:
        funds.write("\nlastTradeDate : ")
        funds.write("\ntimeElapsed : ")


def findStartingCurrency(oppurtunity):
    for key in reversed(list(oppurtunity.keys())):
        if key in stable_currencies: return key
    return None

def getConvRateToStable(fromC, toC, conversion_rates):
    try:
        return math.exp(-1*conversion_rates[fromC][toC]), toC
    except Exception:
        for toCurrency in stable_currencies:
            try:
                return math.exp(-1*conversion_rates[fromC][toCurrency]), toCurrency
            except Exception:
                continue

    return None

def reverse_oppurtunity(oppurtunity):
    new_oppurtunity = {}
    new_oppurtunity['stable'] = oppurtunity.pop('stable')
    for key, value in oppurtunity.items():
        new_oppurtunity[value] = key
    return new_oppurtunity

def getSymbol(fromC, toC, exchange):
    if (fromC + "/" + toC) in exchange.symbols: return (fromC + "/" + toC)
    else: return (toC + "/" + fromC)

def getBalance(exchange, curr):
    if actuallyMakeTransactions: return exchange.fetch_balance()[curr]['free']
    elif simulateWithTestFunds: return getTestFundsBalance(exchange.id + "_" + curr)
    else: return inf

def getMaxes(oppurtunity, conversion_rates, exchange, maxSize, stableCurrency):
        maxTheoreticalAmount = inf
        maxPracticalAmount = max_investment[exchange.id]
        currentCurrency = stableCurrency
        maxPracticalAmount = min(getBalance(exchange, currentCurrency), maxPracticalAmount)

      #while there are still conversions left, pop the next step and convert
        while(len(oppurtunity.items()) > 0):
            nextCurrency = oppurtunity.pop(currentCurrency, None)
            if nextCurrency == None: break
            rate, newStable = getConvRateToStable(currentCurrency, stableCurrency, conversion_rates)
            if (maxTheoreticalAmount > (maxSize[currentCurrency][nextCurrency] * rate / (1-conversion_rates['fee'])) or maxPracticalAmount > (maxSize[currentCurrency][nextCurrency] * rate / (1-conversion_rates['fee']))): limiting_conversion = currentCurrency + " to " + nextCurrency
            maxTheoreticalAmount = min(maxTheoreticalAmount, maxSize[currentCurrency][nextCurrency] * rate / (1-conversion_rates['fee']))
            maxPracticalAmount = min(maxPracticalAmount, maxSize[currentCurrency][nextCurrency] * rate / (1-conversion_rates['fee']))
            currentCurrency = nextCurrency

        #make sure we end up with a stable currency (in case we had to append entry conversion)
        if (currentCurrency != stableCurrency):
            rate, newStable = getConvRateToStable(currentCurrency, stableCurrency, conversion_rates)
            stableCurrency = newStable
            nextCurrency = stableCurrency
            if (maxTheoreticalAmount > (maxSize[currentCurrency][nextCurrency] * rate / (1-conversion_rates['fee'])) or maxPracticalAmount > (maxSize[currentCurrency][nextCurrency] * rate / (1-conversion_rates['fee']))): limiting_conversion = currentCurrency + " to " + stableCurrency
            maxTheoreticalAmount = min(maxTheoreticalAmount, maxSize[currentCurrency][nextCurrency] * rate / (1-conversion_rates['fee']))
            maxPracticalAmount = min(maxPracticalAmount, maxSize[currentCurrency][nextCurrency] * rate / (1-conversion_rates['fee']))
            currentCurrency = stableCurrency
        
        return maxPracticalAmount, maxTheoreticalAmount, limiting_conversion

def priceToPrecision(symbol, x):
    pair = symbol.replace("/", "_")
    for dic in precisionData:
            if pair == dic['pair']:
                precision = dic['decimal']
    return floor_decimal(x, precision)

def floor_decimal(x, places):
    return int(x * (10 ** places)) / 10 ** places

def amountToPrecision(symbol, x):
    pair = symbol.replace("/", "_")
    for dic in precisionData:
            if pair == dic['pair']:
                precision = dic['amount_scale']
    return floor_decimal(x, precision)

def exploreOppurtunities(oppurtunities, conversion_rates, exchange, maxSize, recursiveCall=0, unexplored=False):
    for oppurtunity in oppurtunities:
        try:
            limiting_conversion = ""
            if unexplored:
                log("UNEXPLORED OPPURTUNITY!  >  " + str(oppurtunity), False, False)
            elif recursiveCall > 0: 
                log("OPPURTUNITY FOUND AFTER " + str(recursiveCall) + " COMPROMISE(S)!  >  " + str(oppurtunity), False, False)
            else:
                log("OPPURTUNITY!  >  " + str(oppurtunity), False, False)
            stableCurrency = oppurtunity.pop('stable', None)
            if stableCurrency not in oppurtunity.keys():
                stableCurrency = findStartingCurrency(oppurtunity)
            if stableCurrency == None:
                stableCurrency = 'USDT'
                entryCurrency = list(oppurtunity.keys())[ len(list(oppurtunity.keys()))-1 ]
                oppurtunity[stableCurrency] = entryCurrency
                log("  >   OPPURTUNITY HAS NO STABLE STARTING POINT. APPENDING ENTRY CONVERSION: " + stableCurrency + " to " + entryCurrency)

            oppurtunityCopy = copy.deepcopy(oppurtunity)
            oppurtunityCopy['stable'] = stableCurrency
            currentCurrency = stableCurrency

            maxPracticalAmount, maxTheoreticalAmount, limiting_conversion = getMaxes(copy.deepcopy(oppurtunity), conversion_rates, exchange, maxSize, stableCurrency)
            symbol = getSymbol(currentCurrency, oppurtunity[currentCurrency], exchange)
            maxPracticalAmount = amountToPrecision(symbol, maxPracticalAmount)
            maxTheoreticalAmount = amountToPrecision(symbol, maxTheoreticalAmount)
            log("    INFO >  STABLE: " + stableCurrency + ", MAX_PRACTICAL: " + str(maxPracticalAmount) + ", MAX_THEORETICAL: " + str(maxTheoreticalAmount), ", LIMITING: " + limiting_conversion)
            value = maxPracticalAmount

            if (value < min_investment[exchange.id]):
                    log("  >   CAN ONLY INVEST " + str(value) + " " + stableCurrency + " INTO THIS OPPURTUNITY. MOST LIMITING CONVERSION IS " + limiting_conversion)
                    if recursiveCall < maxCompromises and maxTheoreticalAmount < min_investment[exchange.id]: 
                        if (limiting_conversion.split(' to ')[0] + '/' + limiting_conversion.split(' to ')[1]) in exchange.symbols:
                            compromiseConversion = limiting_conversion.split(' to ')[0] + '/' + limiting_conversion.split(' to ')[1]
                        else:
                            compromiseConversion = limiting_conversion.split(' to ')[1] + '/' + limiting_conversion.split(' to ')[0]
                        
                        log("SEARCHING FOR COMPROMISE ON " + compromiseConversion + " >  RECURSIVE CALLS: " + str(recursiveCall), False, False)
                        new_conversion_rates, newMaxSize = loadConversionRates(exchange, conversion_rates['fee'], compromiseConversion, recursiveCall+1, conversion_rates, maxSize)
                        if new_conversion_rates == None or newMaxSize == None: continue
                        new_oppurtunities = findOppurtunity(new_conversion_rates, stableCurrency)
                        if len(new_oppurtunities) != 0:
                            if (exploreOppurtunities(new_oppurtunities, new_conversion_rates, exchange, newMaxSize, recursiveCall+1)): return True
                        else:
                            log("  >   NO OPPURTUNITIES POSSIBLE WITH COMPROMISE.")
                    elif recursiveCall < maxCompromises:
                        log("  >   INVESTMENT LIMITED BY PRACTICAL MAX. (account balance too low)")
                    continue

            #while there are still conversions left, pop the next step and convert
            while(len(oppurtunity.items()) > 0):
                nextCurrency = oppurtunity.pop(currentCurrency, None)
                if nextCurrency == None: break
                symbol = getSymbol(currentCurrency, nextCurrency, exchange)
                if currentCurrency == stableCurrency:
                    maxPracticalAmount = amountToPrecision(symbol, maxPracticalAmount)
                    maxTheoreticalAmount = amountToPrecision(symbol, maxTheoreticalAmount)
                value = amountToPrecision(symbol, value)
                log(" > " + str(value) + " " + currentCurrency + " converts to: " + str(value*math.exp(-1*conversion_rates[currentCurrency][nextCurrency])) + " " + nextCurrency, False, False)
                value = value*math.exp(-1*conversion_rates[currentCurrency][nextCurrency])
                value = amountToPrecision(symbol, value)
                currentCurrency = nextCurrency

            #make sure we end up with a stable currency (in case we had to append entry conversion)
            if (currentCurrency != stableCurrency):
                rate, newStable = getConvRateToStable(currentCurrency, stableCurrency, conversion_rates)
                stableCurrency = newStable
                log(" > " + str(value) + " " + currentCurrency + " converts to: " + str(value*rate) + " " + stableCurrency, False, False)
                value = value*rate
                symbol = getSymbol(currentCurrency, stableCurrency, exchange)
                value = amountToPrecision(symbol, value)
                currentCurrency = stableCurrency

            true_profit = value-maxPracticalAmount
            growth = (true_profit/maxPracticalAmount)*100
            possible_profit = maxTheoreticalAmount*(growth/100)
            log("So we can go from " + str(maxPracticalAmount) + " " + stableCurrency + " to " + str(value) + " " + currentCurrency + ", an increase of " + str(growth) + "%", False, True)
            log("We can theoretically move "+ str(maxTheoreticalAmount) + " " + stableCurrency + " through this conversion for a final profit of approximately: " + str(possible_profit) + " " + stableCurrency )
            log("The conversion which limits our transaction size the most is: " + limiting_conversion)

            if growth <= max_growth and growth >= min_growth and true_profit >= min_profit and maxPracticalAmount >= min_investment[exchange.id]:
                log(exchange.id + "  >  profit of " + str(possible_profit) + " " + stableCurrency + " with investment of " + str(maxTheoreticalAmount) + " " + stableCurrency + ". (" + str(growth) + '% increase). Limited by ' + limiting_conversion + " conversion.", False, True, "profitable_exchanges.txt")
                if simulateWithTestFunds: updateTestFunds(growth, maxPracticalAmount, exchange.id + "_" + stableCurrency)
                if not actuallyMakeTransactions: return True
                return doTransactions(oppurtunityCopy, exchange, maxPracticalAmount, stableCurrency, conversion_rates)
            elif len(oppurtunity.items()) >= 3:
                if (exploreOppurtunities([oppurtunity], conversion_rates, exchange, maxSize, recursiveCall, True)): return True
            else:
                log("  >   OPPURTUNITY IS NOT WORTH EXPLOITING.")


        except Exception as e:
            log("  >   OPPURTUNITY EXPLORATION ERROR " + str(traceback.format_exc()))
            continue

def convert(fromCurrency, toCurrency, exchange, conversion_rates, maxSize):
    try:
        status = None
        if (fromCurrency + "/" + toCurrency) in exchange.symbols:
            symbol = fromCurrency + "/" + toCurrency
            price = (math.exp(-1*conversion_rates[fromCurrency][toCurrency]) / (1-conversion_rates['fee']) )
            amount = min(exchange.fetch_balance()[fromCurrency]['free'], maxSize)
            price = priceToPrecision(symbol, price)
            amount = amountToPrecision(symbol, amount)
            print("sell", amount, fromCurrency, 'for', price, toCurrency, 'a pop')
            status = exchange.create_limit_sell_order(symbol, amount, price, {"timeInForce":"FOK"})

        elif (toCurrency + "/" + fromCurrency) in exchange.symbols:
            symbol = toCurrency + "/" + fromCurrency
            price = 1/(math.exp(-1*conversion_rates[fromCurrency][toCurrency]) / (1-conversion_rates['fee']) )
            cost = exchange.fetch_balance()[fromCurrency]['free']
            amount = min(cost/price, maxSize/price)
            price = priceToPrecision(symbol, price)
            amount = amountToPrecision(symbol, amount)
            print("buy", amount, toCurrency, "for", price, fromCurrency, "a pop")
            status = exchange.create_limit_buy_order(symbol,  amount, price, {"timeInForce":"FOK"})
        
        print(status)
        return status['status']=="closed"
    except Exception as e:
        log("  >   " + fromCurrency + " / " + toCurrency + " CONVERSION ERROR: " + str(traceback.format_exc()))
        return False

def doTransactions(oppurtunity, exchange, maxAmount, stableCurrency, conversion_rates):

    try:

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
            if currentCurrency in stable_currencies: success = convert(currentCurrency, nextCurrency, exchange, conversion_rates, maxAmount)
            else: success = convert(currentCurrency, nextCurrency, exchange, conversion_rates, inf)

            if not success:
                if currentCurrency not in stable_currencies: backup = convert(currentCurrency, stableCurrency, exchange, conversion_rates, maxAmount)
                log("  >>>> CONVERSION STEP FAILED: " + currentCurrency + " TO " + nextCurrency + ". ABORTING. CURRENT BALANCE AT: " + exchange.fetch_balance()) 
                if not backup: log("  >>>> COULD NOT RETURN TO STABLE CURRENCY!! (MANUAL FIX REQUIRED) CURRENT CURRENCY: " + currentCurrency + " CURRENT BALANCE AT: " + exchange.fetch_balance())
                return False
            else:
                log("  >>>>  BALANCE AFTER " + currentCurrency + " TO " + nextCurrency + ": " + exchange.fetch_balance())
                currentCurrency = nextCurrency

        #make sure we end up with a stable currency
        if (currentCurrency != stableCurrency):
            success = convert(currentCurrency, stableCurrency, exchange, conversion_rates, inf)
            if not success:
                log("  >>>> CONVERSION STEP FAILED: " + currentCurrency + " TO " + stableCurrency + ". ABORTING. CURRENT BALANCE AT: " + exchange.fetch_balance()) 
                log("  >>>> COULD NOT RETURN TO STABLE CURRENCY!! (MANUAL FIX REQUIRED) CURRENT CURRENCY: " + currentCurrency + " CURRENT BALANCE AT: " + exchange.fetch_balance())
                return False
            log("  >>>>  BALANCE AFTER " + currentCurrency + " TO " + stableCurrency + ": " + exchange.fetch_balance())
            currentCurrency = stableCurrency
        
        #print final account balance
        final_balance = exchange.fetch_balance()[stableCurrency]['free']
        log(" >>>> FINAL BALANCE: " + final_balance + " " + stableCurrency, False, True)
        if final_balance > startingBalance: return True
        else: return False
    except Exception as e:
        log("  >   EXPLOITATION ERROR: ")# + str(traceback.format_exc()))
        return False


def search():
    while True:
        log(' >>>>>>>>>> NEXT ITERATION <<<<<<<<<<', False, True, "profitable_exchanges.txt")
        for exchange, transactionFee in list(exchanges.items()):
            log("\n" + exchange.id, False, True)
            try:
                conversion_rates, maxSize = loadConversionRates(exchange, transactionFee)
                log("CONVERSION RATES LOADED (" + str(len(conversion_rates.keys())) + ")", True, False)
                oppurtunities = findOppurtunity(conversion_rates)
                if len(oppurtunities) == 0:
                    log("NO ARBITRAGE OPPURTUNITIES :(", False, False)
                else:
                    if (exploreOppurtunities(oppurtunities, conversion_rates, exchange, maxSize) and actuallyMakeTransactions): keepExploitingOppurtunity(exchange, transactionFee)
            except Exception as e:
                log("  >   SEARCH ERROR: " + str(traceback.format_exc()))

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
            log("  >   KEEP EXPLOITING ERROR: " + str(traceback.format_exc()), False, False)
            return

############################################
############################################

if __name__ == "__main__":
    try:
        for exchange in exchanges:
            for stable in stable_currencies:
                updateTestFunds(0, 0, exchange.id + "_" + stable, False)

        search()
    except KeyboardInterrupt:
        log(">>>>>>>>>>> USER INTERRUPTION", False, True)
        log("USER INTERRUPTION", False, True, "profitable_exchanges.txt")