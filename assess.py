from datetime import datetime

stable_currencies = ['USDT', 'USDC', 'USD']
exchanges = [ "bibox", "bitmex", "bitrue", "delta", "lbank" ]

def assess():
        assessment = open("assessment.txt", 'w+')
        overallCentsPerHour = 0
        overallTradesPerHour = 0
        for exchange in exchanges:
                totalCentsPerHour = 0
                totalTradesPerHour = 0

                for stable in stable_currencies:
                        centsPerHour = 0
                        tradesPerHour = 0
                        filename = "test_funds/" + exchange + "_" + stable + ".txt"
                        try:
                                funds = open(filename, 'r')
                                for line in funds.readlines():
                                        if line.split(' : ')[0] == 'startDate': startDate = line.split(' : ')[1].rstrip("\n")
                                        if line.split(' : ')[0] == 'initial': initial = float(line.split(' : ')[1])
                                        if line.split(' : ')[0] == 'current': current = float(line.split(' : ')[1])
                                        if line.split(' : ')[0] == 'numTrades': numTrades = int(line.split(' : ')[1])
                                funds.close()

                                start = datetime.strptime(startDate,"%m/%d/%Y, %H:%M:%S")
                                now = datetime.now()
                                measurementPeriodHours = (now-start).total_seconds()/3600

                                profit = current - initial
                                centsPerHour = (profit/measurementPeriodHours)*100
                                tradesPerHour = numTrades/measurementPeriodHours
                                measurementPeriod = now-start
                                totalTradesPerHour += tradesPerHour
                                totalCentsPerHour += centsPerHour

                        except Exception:
                                continue
                
                overallCentsPerHour += totalCentsPerHour
                overallTradesPerHour += totalTradesPerHour
                assessment.write(exchange + "\n   >   Cents Per Hour: " + str(totalCentsPerHour) + "\n   >   Trades Per Hour: " + str(totalTradesPerHour) + "\n\n")


        assessment.write("\n\n All Exchanges Combined:\n   >   Cents Per Hour: " + str(overallCentsPerHour) + "\n   >   Trades Per Hour: " + str(overallTradesPerHour) + "\n\n")
        assessment.write("\n\nMeasurement Period: " + str(datetime.utcfromtimestamp(measurementPeriod.total_seconds()).strftime("%H hours, %M minutes, %S seconds")))
        assessment.close()


if __name__ == "__main__":
        assess()