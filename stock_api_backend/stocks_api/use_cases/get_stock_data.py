import requests
from decouple import config

#environment variable setup
#TODO replace these with the company API keys, right now it just uses my personal key
fmp_api_key=config('FMP_API_KEY')
eodhd_api_key=config('EODHD_API_KEY')

#FMP and EOD require different inputs for the API requests
#Below function pre-processes stock data taken from the API to return identical result formats

def fetch_stock_data_fmp(input_ticker):
    url='https://financialmodelingprep.com/api/v3/discounted-cash-flow/'+input_ticker+'?apikey='+fmp_api_key
    response=requests.get(url)
    if response.status_code==200:
        print('Successful FMP response')
        return 200,response.json()[0]
    print('Failed to fetch FMP response')
    return response.status_code,None

def fetch_stock_data_eodhd(input_ticker):
    #EODHD demo API key only allows access to AAPL stock calls
    url='https://eodhd.com/api/real-time/'+input_ticker+'?api_token='+eodhd_api_key+'&fmt=json'
    response=requests.get(url)
    if response.status_code==200:
        print('Successful EODHD response')
        return 200,response.json()
    print('Failed to fetch EODHD response')
    return response.status_code,None