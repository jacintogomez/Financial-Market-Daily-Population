from urllib import response
import requests
from decouple import config
from datetime import datetime,timezone
from ..domain.models import Stock
from ..interfaces.mongodb_handler import is_asset_in_mongo

# Environment variable setup

fmp_api_suffix='apikey='+config('FMP_API_KEY')
eod_api_suffix='api_token='+config('EODHD_API_KEY')+'&fmt=json'

# API Urls
fmp_api_prefix='https://financialmodelingprep.com/api/'
eod_api_prefix='https://eodhd.com/api/'

fmp_urls=[
    'v3/quote/',
    'v4/pre-post-market-trade/',
]

eod_urls=[
    'fundamentals/',
]

def fmp_contains(symbol):
    temp=is_asset_in_mongo(symbol)
    if temp:
        print('asset is in mongodb under FMP')
    else:
        print('asset is not in mongodb under FMP')
    return temp

def eod_contains(symbol):
    pass
    # temp,exchange=is_asset_in_mongo_if_so_get_exchange(symbol)
    # if temp:
    #     print('asset is in mongodb under EOD')
    # else:
    #     print('asset is not in mongodb under EOD')
    # return temp,exchange

def fetch_stock_data(input_ticker,provider):
    today=datetime.now().strftime('%Y-%m-%d')

    stock=Stock(symbol=input_ticker,provider=provider)
    stock_data={'data':{}}
    urls=fmp_urls if provider=='FMP' else eod_urls
    data_retrieved=False

    for url in urls:
        full_url=f'{fmp_api_prefix}{url}{input_ticker}?{fmp_api_suffix}' if provider=='FMP' else f'{eod_api_prefix}{url}{input_ticker}?{eod_api_suffix}'
        print('full_url=',full_url)
        response=requests.get(full_url)
        if response.status_code==200:
            apidata=response.json()
            print('apidata=',apidata)
            key=url.split('/')[-2]
            if isinstance(apidata,list) and apidata:
                data_retrieved=True
                print('key is ',key)
                stock_data['data'][key]=apidata[0]
            elif apidata:
                data_retrieved=True
                stock_data['data'][key]=apidata

    if data_retrieved:
        print('upserting')
        stock.upsert_stock(input_ticker,stock_data['data'])
    print(stock.to_dict())
    return 200,stock

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
    url=eod_api_prefix+'exchange-symbol-list/'+market_ticker+'?'+eod_api_suffix
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
    url=eod_api_prefix+'exchanges-list/?'+eod_api_suffix
    response=requests.get(url)
    if response.status_code==200:
        return 200,response.json()
    return response.status_code,None

