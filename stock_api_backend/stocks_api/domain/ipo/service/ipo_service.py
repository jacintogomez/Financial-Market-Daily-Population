from decouple import config
import requests

fmp_api_suffix='apikey='+config('FMP_API_KEY')
fmp_api_prefix='https://financialmodelingprep.com/api/'

urls=[
    'v4/ipo-calendar-confirmed',
    'v4/ipo-calendar-prospectus',
    'v3/ipo-calendar',
]

def fetch_ipo_calendar_data():
    ipo_data={
        'IPO Confirmed':{},
        'IPO Prospectus':{},
    }
    confirmed_url=f'{fmp_api_prefix}v4/ipo-calendar-confirmed?{fmp_api_suffix}'
    prospectus_url=f'{fmp_api_prefix}v4/ipo-calendar-prospectus?{fmp_api_suffix}'
    response1=requests.get(confirmed_url)
    response2=requests.get(prospectus_url)
    if response1.status_code==200:
        apidata=response1.json()
        #print('apidata=',apidata)
        if isinstance(apidata,list) and apidata:
            ipo_data['IPO Confirmed']=apidata
    if response2.status_code==200:
        apidata=response2.json()
        #print('apidata=',apidata)
        if isinstance(apidata,list) and apidata:
            ipo_data['IPO Prospectus']=apidata
    return 200,ipo_data