from urllib import response

import requests
from decouple import config
from datetime import datetime,timezone
from ..domain.models import Stock

# Environment variable setup

fmp_api_suffix='apikey='+config('FMP_API_KEY')
eodhd_api_suffix='api_token='+config('EODHD_API_KEY')+'&fmt=json'

# API Urls
fmp_api_prefix='https://financialmodelingprep.com/api/'
eodhd_api_prefix='https://eodhd.com/api/'

all_urls=[
    'v3/quote/',
    'v4/pre-post-market-trade/',
]

def fetch_stock_data_fmp(input_ticker):
    today=datetime.now().strftime('%Y-%m-%d')

    stock=Stock(symbol=input_ticker,provider='FMP')
    stock_data={'data':{}}

    for url in all_urls:
        full_url=f'{fmp_api_prefix}{url}{input_ticker}?{fmp_api_suffix}'
        print('full_url=',full_url)
        response=requests.get(full_url)
        if response.status_code==200:
            apidata=response.json()
            print('apidata=',apidata)
            key=url.split('/')[-2]
            if isinstance(apidata,list) and apidata:
                print('key is ',key)
                stock_data['data'][key]=apidata[0]
            elif apidata:
                stock_data['data'][key]=apidata
    stock.upsert_stock(input_ticker,stock_data['data'])
    print(stock.to_dict())
    return 200,stock

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

