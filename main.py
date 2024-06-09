from stockdex import TickerFactory
import datetime
import customtkinter as ctk

ticker = TickerFactory(ticker="BHP.AX", data_source="yahoo_api").ticker
data = ticker.price(range='200y', dataGranularity='1d').to_dict()

timestamps: dict = data["timestamp"]
prices: dict = data["close"]

key_dates = {}

for timestamp, price in zip(timestamps, prices):
    if "-06-30" in str(timestamps[timestamp]):
        key_dates[timestamps[timestamp]] = prices[price]

print(key_dates[datetime.datetime(2020, 6, 30)])


root = ctk.CTk()
root.mainloop()
