from decouple import config
import requests
from ..model.models import IPO

fmp_api_suffix='apikey='+config('FMP_API_KEY')
fmp_api_prefix='https://financialmodelingprep.com/api/'

urls=[
    'v4/ipo-calendar-confirmed',
    'v4/ipo-calendar-prospectus',
    'v3/ipo-calendar',
]

def fetch_ipo_calendar_data():
    ipo_data={'data':{}}
    for url in urls:
        full_url=f'{fmp_api_prefix}{url}?{fmp_api_suffix}'
        print('full_url=',full_url)
        response=requests.get(full_url)
        if response.status_code==200:
            apidata=response.json()
            #print('apidata=',apidata)
            key=url.split('/')[-1]
            print('key is ',key)
            if isinstance(apidata,list) and apidata:
                print(apidata[0])
                ipo_data['data'][key]=apidata
    return 200,ipo_data