Have BTC and USD to buy/sell on several exchanges
if the price difference between two exchanges is big enough to make up ofr transaction costs then buy BTC on cheap exchange and sell same amount of BTC on expensive one. Then you have the same amount of BTC but more USD.


OR on only one exchange, transfer money between currencies to make profit
	e.g. convert money from USD -> some combinations of currencies -> USD to make profit on inconsistencies in market



exchanges:
binance (2nd strat)
gemini

CCXT library for exchanges


NEXT STEPS:
put market data into SQL and keep only relevant info
also use SQL to understand and find the data we need
bring data back into python

useful data is:
1. ARBITRAGE: buy/sell price (compared to USD), for each market, for each crypto we want AND transaction fees

2. TRIANGULAR: conversion rates between each crypto pair we want and for that crypto to USD




BEFORE CODE SAVING HERE JUST IN CASE


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