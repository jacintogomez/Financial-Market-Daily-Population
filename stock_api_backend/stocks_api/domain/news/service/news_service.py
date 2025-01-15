from decouple import config
from http import HTTPStatus
import requests
from requests import RequestException
from ...apiresponse.model.models import APIResponse

eod_api_prefix='https://eodhd.com/api/'
eod_api_suffix='api_token='+config('EODHD_API_KEY')+'&fmt=json'

urls=[
    'news',
]

def validate_api_response(data):
    print('validating news')
    if data is None:
        return None
    if isinstance(data,list):
        if not data:
            return None
        return data[0]
    if isinstance(data,dict):
        if not data:
            return None
        return data
    return None

def fetch_news_data(symbol,market):
    if not symbol:
        APIResponse(int(HTTPStatus.BAD_REQUEST),{},'No symbol provided')
    news_data={}
    def make_request(url,endpoint):
        full_url=f'{eod_api_prefix}{url}?s={symbol}.{market}&offset=0&limit=10&{eod_api_suffix}'
        print('full_url=',full_url)
        try:
            response=requests.get(full_url)
            if response.status_code==HTTPStatus.NOT_FOUND:
                return False,f'Endpoint {url} not found',None
            response.raise_for_status()
            try:
                data=response.json()
            except requests.exceptions.JSONDecodeError as e:
                return False,f'Invalid JSON response {e} from {url}',None
            validate_data=validate_api_response(data)
            if validate_data is not None:
                return True,'',validate_data
            return False,f'No valid data returned from {url}',None
        except requests.exceptions.HTTPError as e:
            return False,f'HTTP error {e} occurred from {url}',None
        except RequestException as e:
            return False,f'Request exception {e} occurred from {url}',None
    try:
        successes=0
        total_endpoints=len(urls)
        errors=[]
        for url in urls:
            print('url ishjh ',url)
            endpoint_key=url
            print('name is ',endpoint_key)
            status,error,data=make_request(url,endpoint_key)
            print('status is ',status)
            if status:
                news_data[endpoint_key]=data
                successes+=1
            else:
                errors.append(error)
        if successes==0:
            print('no news data')
            return APIResponse(int(HTTPStatus.SERVICE_UNAVAILABLE),f'Failed to fetch data for symbol {symbol}',{})
        if not news_data:
            return APIResponse(int(HTTPStatus.NO_CONTENT),f'No valid data received for symbol {symbol}',{})
        if successes<total_endpoints:
            return APIResponse(int(HTTPStatus.PARTIAL_CONTENT),f'Could not retrieve data for all {symbol} endpoints: {errors}',news_data)
        return APIResponse(int(HTTPStatus.OK),f'Successfully retrieved data for {symbol}',news_data)
    except Exception as e:
        return APIResponse(int(HTTPStatus.INTERNAL_SERVER_ERROR),f'Failed to fetch data for symbol {symbol}, Exception: {e}',{})