import requests
from decouple import config

#environment variable setup
fmp_api_key=config('FMP_API_KEY')
eodhd_api_key=config('EODHD_API_KEY')

class Stock:
    def __init__(self,ticker,name=None,isin=None,country_code=None):
        self.ticker = ticker
        self.name = name
        self.isin=isin
        self.country_code = country_code
    def __str__(self):
        return self.name+' ('+self.ticker+')'

#FMP and EOD require different inputs for the API requests
#Below function pre-processes stock data to store in an object

def fetch_stock_data_fmp(input_ticker):
    stock=Stock(input_ticker)
    url='https://financialmodelingprep.com/api/v3/discounted-cash-flow/'+stock.ticker+'?apikey='+fmp_api_key
    response=requests.get(url)
    if response.status_code==200:
        data=response.json()
        return {
            'response_code':response.status_code,
            'ticker':data[0]['symbol'],
            'price':data[0]['Stock Price'],
        }
    return {'response_code':response.status_code}

def fetch_stock_data_eodhd(input_ticker):
    stock=Stock(input_ticker)
    url='https://eodhd.com/api/real-time/'+stock.ticker+'?api_token='+eodhd_api_key+'&fmt=json'
    response=requests.get(url)
    if response.status_code==200:
        data=response.json()
        return {
            'response_code':response.status_code,
            'ticker':data['code'],
            'price':data['close'],
        }
    return {'response_code':response.status_code}