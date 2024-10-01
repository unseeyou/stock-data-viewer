from stockdex import Ticker
import FreeSimpleGUI as sg
import openpyxl as xl
from pprint import pprint
from get_tickers import lookup_all_tickers

file = sg.popup_get_file("Select File", file_types=(("Excel Files", "*.xlsx"), ("All Files", "*.*")))
print(file)
# file = "sample.xlsx"

wb = xl.load_workbook(filename=file, data_only=False)
sheet = wb["Listed share price"]

date = sheet["G3"].value.year

# where the current stock unit prices are located
stock_values_loc = ["E", 6]
data = sheet["".join([str(i) for i in stock_values_loc])].value
while data is not None:
    stock_values_loc[1] += 1
    data = sheet["".join([str(i) for i in stock_values_loc])].value

print("Loading companies...", end="")
companies_loc = ["A", 6]
companies = []
data = sheet["".join([str(i) for i in companies_loc])].value
while data is not None:
    companies_loc[1] += 1
    data = sheet["".join([str(i) for i in companies_loc])].value
    if data is not None:
        companies.append(data)
companies = lookup_all_tickers(companies)
pprint(companies)
print(" DONE!")

total_stocks = stock_values_loc[1] - 6

company_tickers = []
company_values = []

for i in range(total_stocks):
    if sheet[f"H{i + 6}"].value is not None:
        company_tickers.append(sheet[f"H{i + 6}"].value)
    else:
        val = companies[sheet[f"A{i + 6}"].value]
        company_tickers.append(val)
        sheet[f"H{i + 6}"] = val

print(company_tickers)


for company in company_tickers:
    if company is not None and company != "SPK.AX":
        print(f"Getting stock data for {company}...", end="")
        final_price = -1

        ticker = Ticker(ticker=company)
        data = ticker.yahoo_api_price(range='200y', dataGranularity='1d').to_dict()

        timestamps: dict = data["timestamp"]
        # pprint(timestamps)
        prices: dict = data["close"]

        for timestamp, price in zip(timestamps, prices):
            if f"{date}-06-30" in str(timestamps[timestamp]):
                final_price = prices[price]
                break
            elif date == 2024 and f"{date}-06-28" in str(timestamps[timestamp]):
                final_price = prices[price]
                break

        output = (company, round(final_price, 2)) if final_price != -1 else (company, "N/A")
        print(" DONE!")
        print(output)

    else:
        output = (company, "N/A")
    company_values.append(output)

print("Adding values to spreadsheet...", end="")
for cell in range(len(company_values)):
    price_pos = f"E{cell + 6}"
    sheet[price_pos] = company_values[cell][1]
print(" DONE!")

wb.save(filename=file)
