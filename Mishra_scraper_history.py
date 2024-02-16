# e.g. run script in terminal: python <filename>.py TSLA AMZN AAPL META NFLX GOOG PLNT WMT MSFT F
import json
import csv
import sys
from typing import Any, Dict
import requests
from bs4 import BeautifulSoup
import pandas as pd
import yfinance as yf
from datetime import date
def get_data(ticker_symbol: Any) -> Dict[str, Any]:
 print('Getting history data of ', ticker_symbol)
 tdg = yf.Ticker(ticker_symbol)
 data = tdg.history(interval ='1d', start = '2010-02-01', end = '2024-02-04')
 data = data.reset_index().rename(columns={"index":"date"})	
 data['Date'] = pd.to_datetime(data['Date']).dt.date
 print(data.head())
 headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'} 
 # Construct URL for the given ticker_symbol
 url = f'https://finance.yahoo.com/quote/{ticker_symbol}/holders'
 # Make a request to the URL
 r = requests.get(url, headers=headers)
 soup = BeautifulSoup(r.text, 'html.parser')
 data = data.assign(stock_name =soup.find('div', {'class':'D(ib) Mt(-5px) Maw(38%)--tab768 Maw(38%) Mend(10px) Ov(h) smartphone_Maw(85%) smartphone_Mend(0px)'}).find_all('div')[0].text.strip())
 stock_column = data.pop('stock_name')
 data.insert(0,'stock_name',stock_column) 
 return data

# Check if ticker symbols are provided as command line arguments
if len(sys.argv) < 2:
 print("Usage: python script.py <ticker_symbol1> <ticker_symbol2> ...")
 sys.exit(1)
# Extract ticker symbols from command line arguments
ticker_symbols = sys.argv[1:]
# Get stock data for each ticker symbol
stockdata = pd.DataFrame()
for symbol in ticker_symbols:
 #get_data(symbol)
 stockdata = pd.concat([stockdata,get_data(symbol)], ignore_index = True)

# Writing stock data to a JSON file
with open('history_data.json', 'w', encoding='utf-8') as f:
 data = stockdata.to_json(orient='index')
 json.dump(data, f)

# Writing stock data to a CSV file with aligned values
CSV_FILE_PATH = 'history_data.csv'
stockdata.to_csv(CSV_FILE_PATH, index = False)


# Writing stock data to an Excel file
EXCEL_FILE_PATH = 'history_data.xlsx'
stockdata.to_excel(EXCEL_FILE_PATH, index=False)
print('Done!')