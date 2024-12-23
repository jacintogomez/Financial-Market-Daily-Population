from decouple import config
import requests

eod_api_prefix='https://eodhd.com/api/'
eod_api_suffix='api_token='+config('EODHD_API_KEY')+'&fmt=json'

urls=[
    'fundamentals/',
]

def fetch_fundamentals_data(symbol):
    fundamentals_data={}
    for url in urls:
        full_url=f'{eod_api_prefix}{url}{symbol}?{eod_api_suffix}'
        print('full_url=',full_url)
        response=requests.get(full_url)
        if response.status_code==200:
            apidata=response.json()
            key=url.split('/')[-2]
            if isinstance(apidata,list) and apidata:
                fundamentals_data[key]=apidata[0]
            elif apidata:
                fundamentals_data[key]=apidata

    return 200,fundamentals_data