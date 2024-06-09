import mini_yahoo_finance as yfinance
import pandas as pd

df = yfinance.get_stock_df(
    stock_name="BHP.AX",
    start_date="30-06-2020",
    end_date="01-07-2020",
)

print(df)
