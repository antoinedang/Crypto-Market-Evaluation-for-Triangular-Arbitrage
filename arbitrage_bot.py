import ccxt
import numpy as np
import math
import time
from datetime import datetime
import copy
import traceback

currencies = ['ETH', 'BTC', 'ADA', 'XLM', 'XMR', 'SOL', 'LTC', 'USDK', 'DAI', 'USDC', 'USDT', 'AVAX', 'BNB', 'XRP', 'DOT', 'BCH', 'USD', 'UST', 'MATIC', 'SHIB', 'DOGE', 'LINK', 'BIX', 'TRX', 'SAND', 'BAC', 'JWL', 'WEC', 'AAVE', 'ZEC', '1INCH', 'GERA', 'REV', 'SPUT', 'EUR'] #currencies we care about
quote_currencies = ['ETH', 'BTC', 'USDT', 'USDC', 'USDK', 'DAI', 'USD', 'UST', 'EUR'] #quote currencies
stable_currencies = ['USDT', 'USDC', 'USD'] #all conversions start and end in these currencies (what we can trade with)
maxCompromises = 3 # how many maximum compromises (a compromise is when we take the next best price on the most limiting conversion rather than just the best price)
currency_pairs = [ x + '/'+ y for x in currencies for y in currencies if x != y ]
min_profit = 0.01 #the conversion must make at least one cent USD profit to be considered worth it
min_investment = { 'bitmex':100, 'bitrue':38, 'bibox':1, 'lbank':50, 'delta':50 } #we'll only consider transactions we can invest at least this amount of US dollars into
useAllExchangeCurrencies = False #uses all available currency pairs that have a quote currency in our quote currencies list

simulateWithTestFunds = True
initialTestFundsDefault = 100

actuallyMakeTransactions = False

inf = 9999999
lastLog = time.time()

aax = ccxt.aax({'secret':'f7591aa3c2c63c52110cf87cb98a6ed1', 'apiKey':'a0zty4VLfxxqOOQ1gQgnJ9URNo'})
btcalpha = ccxt.btcalpha({'secret':'63hWe1ydFj8L9t6vspZbawYhmmD9WT9xdgy5175XZv8s93SvsNddaMVv6B1irf1mxqknWksEYAhCv7BTQu2pmkJx', 'apiKey':'4poAAqfmJGq3bQEzcWdC9m4wx7bXnLGyuuQyQqgUvikdheAoV8B2orgQiMrVaEA8HAYVc3SDRh92'})


bigone = ccxt.bigone()
bibox = ccxt.bibox()
binance = ccxt.binance({
    #'apiKey':'CVmVNcQEK9JK3XxoDZq6KGuUmEkvJhhxuTpmyD35SDaey4ASetMEHLaXX4kLZTGk',
    #'secret':'ShmGL7VxeVlDTFjJuOGFGuFf2kHaki8Ub0LM08YINwFtyRIm7pcq9emuXzfgeMEn',
    #'enableRateLimit': True,
    #'options': {'createMarketBuyOrderRequiresPrice': False }
})
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
kucoin = ccxt.kucoin({'password':'Ilove2fly%percent%', 'secret':'25608af7-631f-4a4f-a0ec-e225f6f3b2e0', 'apiKey':'61cb4d0e895c6300011ef6ae'})
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
wavesexchange = ccxt.wavesexchange()
whitebit = ccxt.whitebit()
xena = ccxt.xena()
yobit = ccxt.yobit()
zaif = ccxt.zaif()
zb = ccxt.zb()
zipmex = ccxt.zipmex()
zonda = ccxt.zonda()


other_exchanges = { kucoin:0.001, ascendex:0.002, bequant:0.001, bitbank:0.0015, bitbns:0.0025, bitcoincom:0.0075, bitfinex:0.002, bitfinex2:0.002, bitflyer:0.002, bitforex:0.001, bitget:0.001, bithumb:0.0015, bitmart:0.0025, bitpanda:0.0015, bitso:0.001, bitstamp:0.005, bittrex:0.0035, bitvavo:0.0025, bl3p:0.0026, btcmarkets:0.002, btctradeua:0.001, buda:0.008, bw:0.002, bybit:0.001, cdax:0.002, cex:0.0025, coinbasepro:0.005, coinex:0.002, coinfalcon:0.002, coinmate:0.0035, crex24:0.001, eqonex:0.0009, equos:0.0009, ftx:0.0007, ftxus:0.004, gateio:0.002, huobi:0.002, huobijp:0.002, independentreserve:0.005, indodax:0.003, itbit:0.0035, kraken:0.015, kuna:0.0025, latoken:0.005, latoken1:0.005, liquid:0.0015, luno:0.001, mexc:0.002, ndax:0.002, novadax:0.0025, oceanex:0.001, okcoin:0.0125, okex3:0.001, okex5:0.001, paymium:0.005, phemex:0.001, poloniex:0.00155, probit:0.002, ripio:0, therock:0.002, tidebit:0.003, tidex:0.001, timex:0.005, xena:0.001, zaif:0.002, zb:0.002, zipmex:0.002, zonda:0.0043, lykke:0.0, btcturk:0.0009, btcalpha:0.002, aax:0.001, exmo:0.003, hitbtc3:0.0009, hitbtc:0.0009, whitebit:0.001, yobit:0.002, gemini:0.0035, binanceus:0.001, upbit:0.002, bigone:0.002, idex:0.0025, stex:0.002, okex:0.001, digifinex:0.002, binance:0.001 }

confirmed_exchanges = { bitmex:0.0005, lbank:0.001, bitrue:0.0015, bibox:0.002, delta:0.0005 }

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
            maxSize[curr] = { curr:9999 }

    global currency_pairs

    if useAllExchangeCurrencies:
        currency_pairs = markets.keys()

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

                print("        " + exchange.id, { 'pair': pair, 'highest bid': bid, 'lowest ask': ask, 'maxBidSize':maxBidSize, 'maxAskSize':maxAskSize })

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

def updateTestFunds(growthPercent, maxTransaction, name, countAsTrade=True):
    try:
        funds = open("test_funds/" + name + ".txt", 'r')
        for line in funds.readlines():
            if line.split(' : ')[0] == 'startDate': startDate = line.split(' : ')[1].rstrip("\n")
            if line.split(' : ')[0] == 'initial': initial = float(line.split(' : ')[1])
            if line.split(' : ')[0] == 'current': current = float(line.split(' : ')[1])
            if line.split(' : ')[0] == 'numTrades': numTrades = int(line.split(' : ')[1])
            if not countAsTrade and line.split(' : ')[0] == 'lastTradeDate': lastTradeDate = line.split(' : ')[1].rstrip("\n")
        funds.close()
    except Exception:
        startDate = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        initial = initialTestFundsDefault
        current = initial
        numTrades = 0
    
    if countAsTrade: numTrades += 1
    amountToInvest = min(current, maxTransaction)
    current = current + amountToInvest*(growthPercent/100)

    funds = open("test_funds/" + name + ".txt", 'w+')
    funds.write("startDate : " + startDate)
    funds.write("\ninitial : " + str(initial))
    funds.write("\ncurrent : " + str(current))
    funds.write("\nnumTrades : " + str(numTrades))
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
        return math.exp(-1*conversion_rates[fromC][toC])
    except Exception:
        for toCurrency in stable_currencies:
            try:
                return math.exp(-1*conversion_rates[fromC][toCurrency])
            except Exception:
                continue

    return None

def reverse_oppurtunity(oppurtunity):
    new_oppurtunity = {}
    new_oppurtunity['stable'] = oppurtunity.pop('stable')
    for key, value in oppurtunity.items():
        new_oppurtunity[value] = key
    return new_oppurtunity

def exploreOppurtunities(oppurtunities, conversion_rates, exchange, maxSize, recursiveCall=0, reverse=False):
    for oppurtunity in oppurtunities:
        try:
            limiting_conversion = ""
            oppurtunityCopy = copy.deepcopy(oppurtunity)
            maxAmount = 999999999
            value = 1.0
            if reverse:
                log("REVERSE OPPURTUNITY!  >  " + str(oppurtunity), False, False)
            elif recursiveCall > 0: 
                log("OPPURTUNITY FOUND AFTER " + str(recursiveCall) + " COMPROMISE(S)!  >  " + str(oppurtunity), False, False)
            else:
                log("OPPURTUNITY!  >  " + str(oppurtunity), False, False)
            stableCurrency = oppurtunity.pop('stable')
            if stableCurrency not in oppurtunity.keys():
                stableCurrency = findStartingCurrency(oppurtunity)
            if stableCurrency == None:
                log("  >   OPPURTUNITY HAS NO STABLE STARTING POINT.")
                continue
            currentCurrency = stableCurrency

            #while there are still conversions left, pop the next step and convert
            while(len(oppurtunity.items()) > 0):
                nextCurrency = oppurtunity.pop(currentCurrency, None)
                if nextCurrency == None: break
                log(" > " + str(value) + " " + currentCurrency + " converts to: " + str(value*math.exp(-1*conversion_rates[currentCurrency][nextCurrency])) + " " + nextCurrency, False, False)
                value = value*math.exp(-1*conversion_rates[currentCurrency][nextCurrency])
                rate = getConvRateToStable(currentCurrency, stableCurrency, conversion_rates)
                if (maxAmount > maxSize[currentCurrency][nextCurrency] * rate / (1-conversion_rates['fee'])): limiting_conversion = currentCurrency + " to " + nextCurrency
                maxAmount = min(maxAmount, maxSize[currentCurrency][nextCurrency] * rate / (1-conversion_rates['fee']))
                currentCurrency = nextCurrency

            #make sure we end up with a stable currency
            if (currentCurrency != stableCurrency):
                log(" 1> " + str(value) + " " + currentCurrency + " converts to: " + str(value*math.exp(-1*conversion_rates[currentCurrency][stableCurrency])) + " " + stableCurrency, False, False)
                value = value*math.exp(-1*conversion_rates[currentCurrency][stableCurrency])
                rate = getConvRateToStable(currentCurrency, stableCurrency, conversion_rates)
                if (maxAmount > maxSize[currentCurrency][nextCurrency] * rate / (1-conversion_rates['fee'])): limiting_conversion = currentCurrency + " to " + stableCurrency
                maxAmount = min(maxAmount, maxSize[currentCurrency][stableCurrency] * rate / (1-conversion_rates['fee']))
                currentCurrency = stableCurrency

            growth = (value-1.0)*100
            possible_profit = maxAmount*(value - 1)
            log("So we can go from 1.0 " + stableCurrency + " to " + str(value) + " " + currentCurrency + ", an increase of " + str(growth) + "%", False, True)
            log("We can move "+ str(maxAmount) + " " + stableCurrency + " through this conversion for a final profit of approximately: " + str(possible_profit) + " " + stableCurrency )
            log("The conversion which limits our transaction size the most is: " + limiting_conversion)

            if possible_profit >= min_profit and maxAmount >= min_investment[exchange.id]:
                log(exchange.id + "  >  profit of " + str(possible_profit) + " " + stableCurrency + " with investment of " + str(maxAmount) + " " + stableCurrency + ". (" + str(growth) + '% increase). Limited by ' + limiting_conversion + " conversion.", False, True, "profitable_exchanges.txt")
                if simulateWithTestFunds: updateTestFunds(growth, maxAmount, exchange.id + "_" + stableCurrency)
                if not actuallyMakeTransactions: return True
                return doTransactions(oppurtunityCopy, exchange, maxAmount, stableCurrency, conversion_rates)
            else:
                if possible_profit < 0 and not reverse and abs(possible_profit) > min_profit:
                    log("DETECTED VIABLE NEGATIVE PROFIT. TRYING OPPURTUNITY IN REVERSE ORDER.")
                    reverse_path = [ reverse_oppurtunity(oppurtunityCopy) ]
                    if exploreOppurtunities(reverse_path, conversion_rates, exchange, maxSize, 0, True): return True
                    log("  >   REVERSE OPPURTUNITY FAILED. MOVING ON.")
                    continue
                if recursiveCall < maxCompromises: 
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
                continue
        except Exception as e:
            log("  >   OPPURTUNITY EXPLORATION ERROR " + str(traceback.format_exc()))
            continue

def convert(fromCurrency, toCurrency, exchange, conversion_rates, maxSize, stableCurrency):
    try:
        status = None
        if (fromCurrency + "/" + toCurrency) in exchange.symbols:
            maxSize = maxSize / (math.exp(-1*conversion_rates[fromCurrency][stableCurrency]) / (1-conversion_rates['fee']))
            print("MaxSize in " + fromCurrency + ": " + str(maxSize))
            symbol = fromCurrency + "/" + toCurrency
            price = (math.exp(-1*conversion_rates[fromCurrency][toCurrency]) / (1-conversion_rates['fee']) )
            price = exchange.price_to_precision(symbol, price)
            amount = min(exchange.fetch_balance()[fromCurrency]['free'], maxSize)
            amount = exchange.amount_to_precision(symbol, amount)
            print("sell", amount, fromCurrency, 'for', price, toCurrency, 'a pop')
            status = exchange.create_limit_sell_order(symbol, amount, price, {"timeInForce":"FOK"})
            #turn it into a limit order with a slightly lower price and make it FOK

        elif (toCurrency + "/" + fromCurrency) in exchange.symbols:
            maxSize = maxSize * (math.exp(-1*conversion_rates[stableCurrency][fromCurrency]) / (1-conversion_rates['fee']))
            print("MaxSize in " + fromCurrency + ": " + str(maxSize))
            symbol = toCurrency + "/" + fromCurrency
            price = 1/(math.exp(-1*conversion_rates[fromCurrency][toCurrency]) / (1-conversion_rates['fee']) )
            price = exchange.price_to_precision(symbol, price)
            cost = exchange.fetch_balance()[fromCurrency]['free']
            amount = min(cost/price, maxSize/price)
            amount = exchange.amount_to_precision(symbol, amount)
            print("buy", amount, toCurrency, "for", price, fromCurrency, "a pop")
            status = exchange.create_limit_buy_order(symbol,  amount, price, {"timeInForce":"FOK"})
            #turn it into a limit order with a slightly higher price and make it FOK
        
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
            success = convert(currentCurrency, nextCurrency, exchange, conversion_rates, maxAmount, stableCurrency)
            if not success:
                if currentCurrency != stableCurrency: success = convert(currentCurrency, stableCurrency, exchange, conversion_rates, exchange.fetch_balance()[currentCurrency]['free'], currentCurrency)
                log("  >>>> CONVERSION STEP FAILED: " + currentCurrency + " TO " + nextCurrency + ". ABORTING. CURRENT BALANCE AT: " + exchange.fetch_balance()) 
                if not success: log("  >>>> COULD NOT RETURN TO STABLE CURRENCY!! (MANUAL FIX REQUIRED) CURRENT CURRENCY: " + currentCurrency + " CURRENT BALANCE AT: " + exchange.fetch_balance())
                return False
            else:
                log("  >>>>  BALANCE AFTER " + currentCurrency + " TO " + nextCurrency + ": " + exchange.fetch_balance())
                currentCurrency = nextCurrency

        #make sure we end up with a stable currency
        if (currentCurrency != stableCurrency):
            success = convert(currentCurrency, stableCurrency, exchange, conversion_rates, exchange.fetch_balance()[currentCurrency]['free'], currentCurrency)
            if not success:
                success = convert(currentCurrency, stableCurrency, exchange, conversion_rates, exchange.fetch_balance()[currentCurrency]['free'], currentCurrency)
                if not success: 
                    log("  >>>> CONVERSION STEP FAILED: " + currentCurrency + " TO " + stableCurrency + ". ABORTING. CURRENT BALANCE AT: " + exchange.fetch_balance()) 
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
        for exchange, transactionFee in list(confirmed_exchanges.items()):
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
        for exchange in confirmed_exchanges:
            for stable in stable_currencies:
                updateTestFunds(0, 0, exchange.id + "_" + stable, False)
        search()   
    except KeyboardInterrupt:
        log(">>>>>>>>>>> USER INTERRUPTION", False, True)
        log("USER INTERRUPTION", False, True, "profitable_exchanges.txt")