import requests
import datetime
import csv
import os

currDate = datetime.datetime(2008, 12, 31)
endDate  = datetime.datetime(2018, 12, 31)

startDate = currDate

rates = []

rates.append(["base","date","currency","rate"])

# iterative process to request all rates

dates = []

while currDate <= endDate:
    api = "https://api.ratesapi.io/api/" + currDate.strftime("%Y-%m-%d") + "?base=USD"
    page  = requests.get(api)

    dayRate = page.json()

    if not (dayRate["date"] in dates):
        rates.append(dayRate)
    currDate = currDate + datetime.timedelta(days=1)
    dates.append(dayRate["date"])

# get all currencies available in the period

currencies = []

k = 0
for rate in rates:
    k = k + 1
    if (k > 1):    # omitting header
        for currency in rate["rates"]:
            if not (currency in currencies):
                currencies.append(currency)

currencies.sort()

# write the CSV

currentDir = os.path.dirname(__file__)
filename   = "usd_rates_from_" + startDate.strftime("%Y_%m_%d") + "_to_" + endDate.strftime("%Y_%m_%d") + ".csv"
filePath   = os.path.join(currentDir, filename)

with open(filePath, 'w', newline='') as csvFile:
    writer = csv.writer(csvFile)
    k = 0
    for rate in rates:
        k = k + 1
        if (k > 1):    # omitting header
            for currency in currencies:
                match = False
                for monthCurrency in rate["rates"]:
                    if (currency == monthCurrency):
                        match = True
                        pass
                if match:
                    l = rate["rates"]
                    v = l[currency]
                    writer.writerow([rate["base"], rate["date"], currency, str(v)])
                # fill some currencies not available in other periods with '-'
                else:
                    writer.writerow([rate["base"], rate["date"], currency, "-"])
        else:
            writer.writerow(rate)    # write header