from stockdex import TickerFactory
import datetime, sys
import customtkinter as ctk
import FreeSimpleGUI as sg


def on_submit():
    file = sg.popup_get_file("Choose a file")
    year = "".join([i for i in year_entry.get() if i.isnumeric()])
    stock = stock_entry.get().upper()
    key_dates = {}
    if year and stock:
        try:
            ticker = TickerFactory(ticker=stock, data_source="yahoo_api").ticker
            data = ticker.price(range='200y', dataGranularity='1d').to_dict()

            timestamps: dict = data["timestamp"]
            prices: dict = data["close"]

            for timestamp, price in zip(timestamps, prices):
                if "-06-30" in str(timestamps[timestamp]):
                    key_dates[str(timestamps[timestamp].year)] = prices[price]

        except Exception as err:
            sg.popup(err, title="Oops! Error Encountered!")
        try:
            output.configure(text=f"\nThe price of {stock} at June 30th of {year} was: {round(key_dates[year], 2)}")
        except KeyError:
            output.configure(text="\nThere is no data for that year!")
    else:
        output.configure(text="\nPlease fill in all the details before searching!")
    return 0


def on_closing():
    if sg.popup_yes_no("Quit", "Do you want to quit?", background_color="red", no_titlebar=True, button_color="darkred").lower() == "yes":
        root.destroy()
        sys.exit()


root = ctk.CTk()
root.title("Stock Viewer")
w = 500  # width for the Tk root
h = 200  # height for the Tk root

# get screen width and height
ws = root.winfo_screenwidth()  # width of the screen
hs = root.winfo_screenheight()  # height of the screen

# calculate x and y coordinates for the Tk root window
x = (ws/2) - (w/2)
y = (hs/2) - (h/2)

# set the dimensions of the screen
# and where it is placed
root.geometry('%dx%d+%d+%d' % (w, h, x, y))

title = ctk.CTkLabel(root, text="\nStock Price Checker\n")
title.pack()

year_entry = ctk.CTkEntry(root, corner_radius=5, placeholder_text="year", width=60)
year_entry.pack()

stock_entry = ctk.CTkEntry(root, corner_radius=5, placeholder_text="stock", width=90)
stock_entry.pack()

submit_button = ctk.CTkButton(root, text="Search", command=lambda: on_submit())
submit_button.pack()

output = ctk.CTkLabel(root, text="\nClick the search button after filling in the details above!")
output.pack()

root.protocol("WM_DELETE_WINDOW", on_closing)

root.mainloop()
sys.exit(222222)