from stockdex import TickerFactory
import datetime, sys
import openpyxl as xl

wb = xl.load_workbook(filename="sample.xlsx")
sheet = wb["Share Revaluation"]
print(sheet)
