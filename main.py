from stockdex import TickerFactory
import datetime, sys
import openpyxl as xl

try:
    wb = xl.load_workbook(filename="output.xlsx")
except FileNotFoundError:
    wb = xl.Workbook()

stock = input("Stock: ")
year = input("Year: ")
print("Loading... ")
try:
    ticker = TickerFactory(ticker=stock, data_source="yahoo_api").ticker
    data = ticker.price(range='200y', dataGranularity='1d').to_dict()

    timestamps: dict = data["timestamp"]
    prices: dict = data["close"]

    key_dates = {}

    for timestamp, price in zip(timestamps, prices):
        if "-06-30" in str(timestamps[timestamp]):
            key_dates[str(timestamps[timestamp].year)] = prices[price]

    output=f"The price of {stock} at June 30th of {year} was: {round(key_dates[year], 2)}"

except KeyError:
    output="There is no data for that year!"

sheet = wb.active
sheet["A1"] = output

wb.save("output.xlsx")

print("Output saved!")
