import requests
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("ALPHAADVANTAGE_APIKEY")

# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
url = 'https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords=tesco&apikey=demo'
r = requests.get(url)
data = r.json()

print(data)