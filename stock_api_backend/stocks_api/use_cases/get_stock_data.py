from urllib import response

import requests
from decouple import config
from datetime import datetime
from ..utils import StockData

# Environment variable setup

fmp_api_suffix='apikey='+config('FMP_API_KEY')
eodhd_api_suffix='api_token='+config('EODHD_API_KEY')+'&fmt=json'

# API Urls
fmp_api_prefix='https://financialmodelingprep.com/api/v3/'
eodhd_api_prefix='https://eodhd.com/api/'

#FMP and EOD require different inputs for the API requests
#Below function pre-processes stock data taken from the API to return identical result formats

def fetch_stock_data_fmp(input_ticker):
    today=datetime.now().strftime('%Y-%m-%d')
    url1=fmp_api_prefix+'quote/'+input_ticker+'?'+fmp_api_suffix
    url2=fmp_api_prefix+'profile/'+input_ticker+'?'+fmp_api_suffix

    response1=requests.get(url1)
    stock_data=StockData(input_ticker)

    if response1.status_code==200:
        data=response1.json()
        if isinstance(data,list) and data:
            stock_data.found=True
            stock_data.provider='FMP'
            stock_data.price=data[0]['price']
            stock_data.day_high=data[0]['dayHigh']
            stock_data.day_low=data[0]['dayLow']
            stock_data.open_price=data[0]['open']
            stock_data.change=data[0]['change']
            stock_data.percent_change=data[0]['changesPercentage']
            stock_data.volume=data[0]['volume']
            stock_data.pe_ratio=data[0]['pe']
    response2=requests.get(url2)
    if response2.status_code==200:
        data=response2.json()
        if isinstance(data,list) and data:
            stock_data.market_cap=data[0]['mktCap']
            stock_data.dividend_yield=data[0]['lastDiv']
    return max(response1.status_code,response2.status_code),stock_data

def fetch_stock_data_eodhd(input_ticker):
    url='https://eodhd.com/api/real-time/'+input_ticker+eodhd_api_suffix
    response=requests.get(url)
    if response.status_code==200:
        return 200,response.json()
    return response.status_code,None

def fetch_all_symbols_from_market(market_ticker):
    """Returns response object in format:
    {
        Exchange:
        Code:
        OperatingMIC:
        Country:
        Currency:
        CountryIS02:
        CountryIS03:
    }"""
    url=eodhd_api_prefix+'exchange-symbol-list/'+market_ticker+'?'+eodhd_api_suffix
    response=requests.get(url)
    if response.status_code==200:
        return 200,response.json()
    return response.status_code,None

def fetch_market_exchange_data():
    """Returns response object in format:
    {
        Code:
        Country:
        Currency:
        Exchange:
        Isin:
        Name:
        type:
    }"""
    url=eodhd_api_prefix+'exchanges-list/?'+eodhd_api_suffix
    response=requests.get(url)
    if response.status_code==200:
        return 200,response.json()
    return response.status_code,None
