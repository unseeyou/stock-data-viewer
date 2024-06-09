from stockdex import TickerFactory
import datetime
import customtkinter as ctk


def on_submit():
    year = "".join([i for i in year_entry.get() if i.isnumeric()])
    stock = stock_entry.get().upper()
    if year and stock:
        try:
            ticker = TickerFactory(ticker=stock, data_source="yahoo_api").ticker
            data = ticker.price(range='200y', dataGranularity='1d').to_dict()

            timestamps: dict = data["timestamp"]
            prices: dict = data["close"]

            key_dates = {}

            for timestamp, price in zip(timestamps, prices):
                if "-06-30" in str(timestamps[timestamp]):
                    key_dates[str(timestamps[timestamp].year)] = prices[price]

        except BaseException:
            output.configure(text="\nOops! Something went wrong!\nPlease check your internet connection and try again.")
        try:
            output.configure(text=f"\nThe price of {stock} at June 30th of {year} was: {key_dates[year]}")
        except KeyError:
            output.configure(text="\nThere is no data for that year!")
    else:
        output.configure(text="\nPlease fill in all the details before searching!")


root = ctk.CTk()
root.title("Stock Viewer")
root.geometry("500x200")

year_entry = ctk.CTkEntry(root, corner_radius=5, placeholder_text="year", width=60)
year_entry.pack()

stock_entry = ctk.CTkEntry(root, corner_radius=5, placeholder_text="stock", width=90)
stock_entry.pack()

submit_button = ctk.CTkButton(root, text="Search", command=lambda: on_submit())
submit_button.pack()

output = ctk.CTkLabel(root, text="\nClick the search button after filling in the details above!")
output.pack()

root.mainloop()
