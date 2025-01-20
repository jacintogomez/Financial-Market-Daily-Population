from urllib import response
import requests
from decouple import config
from datetime import datetime,timezone
from ..domain.models import Asset
from ..db_access.mongodb_handler import is_asset_in_mongo

# Environment variable setup

fmp_api_suffix='apikey='+config('FMP_API_KEY')
fmp_api_prefix='https://financialmodelingprep.com/api/'

eod_api_prefix='https://eodhd.com/api/'
eod_api_suffix='api_token='+config('EODHD_API_KEY')+'&fmt=json'

fmp_urls=[
    'v3/quote/',
    'v4/pre-post-market-trade/',
]

eod_urls=[
    'fundamentals/',
]

market_category_map={}

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

def fetch_stock_data_from_api(symbol,provider):
    today=datetime.now().strftime('%Y-%m-%d')

    stock_data={'data':{}}
    urls=fmp_urls if provider=='FMP' else eod_urls

    for url in urls:
        full_url=f'{fmp_api_prefix}{url}{symbol}?{fmp_api_suffix}' if provider=='FMP' else f'{eod_api_prefix}{url}{symbol}?{eod_api_suffix}'
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

    return 200,stock_data

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

def fetch_fmp_symbols():
    url=f'{fmp_api_prefix}v3/stock/list?{fmp_api_suffix}'
    response=requests.get(url)
    if response.status_code==200:
        return response.status_code,response.json()
    return response.status_code,None