# e.g. run script in terminal: python <filename>.py TSLA AMZN AAPL META NFLX GOOG PLNT WMT MSFT F
import json
import csv
import sys
from typing import Any, Dict
import requests
from bs4 import BeautifulSoup
import pandas as pd
def get_data(ticker_symbol: Any) -> Dict[str, Any]:
 print('Getting holders data of ', ticker_symbol) 
 # Set user agent to avoid detection as a scraper
 headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'} 
 # Construct URL for the given ticker_symbol
 url = f'https://finance.yahoo.com/quote/{ticker_symbol}/holders'
 # Make a request to the URL
 r = requests.get(url, headers=headers)
 soup = BeautifulSoup(r.text, 'html.parser')

 #get the first table
 table = soup.find_all('table')[1]
 soup.find('table',class_ = 'W(100%) BdB Bdc($seperatorColor)')
 w_titles = table.find_all('th')
 world_titles = [title.text.strip() for title in w_titles]
 df = pd.DataFrame(columns = world_titles)
 c_data = table.find_all('tr')
 for row in c_data[1:]:
  r_data = row.find_all('td')
  ind_r_data = [data.text.strip() for data in r_data]
  length = len(df)
  df.loc[length] = ind_r_data
 new_df = df.assign(Category =soup.find('section', {'class':'Pb(30px) smartphone_Px(20px)'}).find_all('h3')[1].text.strip()) 
 cat_column = new_df.pop('Category')
 new_df.insert(0,'Category',cat_column)
 new_df = new_df.assign(stock_name =soup.find('div', {'class':'D(ib) Mt(-5px) Maw(38%)--tab768 Maw(38%) Mend(10px) Ov(h) smartphone_Maw(85%) smartphone_Mend(0px)'}).find_all('div')[0].text.strip())
 stock_column = new_df.pop('stock_name')
 new_df.insert(0,'stock_name',stock_column)

 
 #get the second table
 table2 = soup.find_all('table')[2]
 soup.find('table',class_ = 'W(100%) BdB Bdc($seperatorColor)')
 w_titles = table.find_all('th')
 world_titles = [title.text.strip() for title in w_titles]
 df2 = pd.DataFrame(columns = world_titles)
 g_data = table2.find_all('tr')
 for row in g_data[1:]:
  r_data = row.find_all('td')
  ind_r_data = [data.text.strip() for data in r_data]
  length = len(df2)
  df2.loc[length] = ind_r_data
 df2 = df2.assign(Category = soup.find('section', {'class':'Pb(30px) smartphone_Px(20px)'}).find_all('h3')[2].text.strip()) 
 cat2_column = df2.pop('Category')
 df2.insert(0,'Category',cat2_column)
 df2 = df2.assign(stock_name =soup.find('div', {'class':'D(ib) Mt(-5px) Maw(38%)--tab768 Maw(38%) Mend(10px) Ov(h) smartphone_Maw(85%) smartphone_Mend(0px)'}).find_all('div')[0].text.strip())
 stock_column = df2.pop('stock_name')
 df2.insert(0,'stock_name',stock_column)  

 #merge both tables
 new_df = pd.concat([new_df, df2], ignore_index=True)
 print(new_df)

 table3 = soup.find_all('table')[0]
 soup.find('table',class_ = 'W(100%) BdB Bdc($seperatorColor)')
 g_data = table3.find_all('tr')
 for row in g_data[:]:
  r_data = row.find_all('td')
  ind_r_data = [data.text.strip() for data in r_data]
  column1 = ind_r_data[1]
  new_df = new_df.assign(column1 = ind_r_data[0])
  new_df= new_df.rename(columns={"column1":column1})
 print(new_df.head()) 


 return new_df

# Check if ticker symbols are provided as command line arguments
if len(sys.argv) < 2:
 print("Usage: python script.py <ticker_symbol1> <ticker_symbol2> ...")
 sys.exit(1)
# Extract ticker symbols from command line arguments
ticker_symbols = sys.argv[1:]
# Get stock data for each ticker symbol
stockdata = pd.DataFrame()
for symbol in ticker_symbols:
 stockdata = pd.concat([stockdata,get_data(symbol)], ignore_index = True)

# Writing stock data to a JSON file
with open('holder_data.json', 'w', encoding='utf-8') as f:
 data = stockdata.to_json(orient='index')
 json.dump(data, f)

# Writing stock data to a CSV file with aligned values
CSV_FILE_PATH = 'holder_data.csv'
stockdata.to_csv(CSV_FILE_PATH, index = False)


# Writing stock data to an Excel file
EXCEL_FILE_PATH = 'holder_data.xlsx'
stockdata.to_excel(EXCEL_FILE_PATH, index=False)
print('Done!')