from decouple import config
from http import HTTPStatus
import requests
from requests import RequestException
from ...apiresponse.model.models import APIResponse
from ...apiresponse.controller.fetch_data import form_response_symbol,check_for_problems

eod_api_prefix='https://eodhd.com/api/'
eod_api_suffix='api_token='+config('EODHD_API_KEY')+'&fmt=json'

urls=[
    'fundamentals/',
]

def fetch_fundamentals_data(symbol):
    if not symbol:
        return APIResponse(int(HTTPStatus.BAD_REQUEST),{},'No symbol provided')
    fundamentals_data={}
    def make_request(url):
        full_url=f'{eod_api_prefix}{url}{symbol}?{eod_api_suffix}'
        print('full_url=',full_url)
        try:
            return check_for_problems(full_url,url,symbol)
        except requests.exceptions.HTTPError as e:
            return False,f'HTTP error {e} occurred from {url}',None
        except RequestException as e:
            return False,f'Request exception {e} occurred from {url}',None
    try:
        successes=0
        total_endpoints=len(urls)
        errors=[]
        for url in urls:
            endpoint_key=url.split('/')[-2]
            print('name is ',endpoint_key)
            status,error,data=make_request(url)
            print('status is ',status)
            if status:
                fundamentals_data[endpoint_key]=data
                successes+=1
            else:
                errors.append(error)
        apiresponse=form_response_symbol(successes,symbol,'Fundamentals',fundamentals_data,total_endpoints,errors)
        return apiresponse
    except Exception as e:
        return APIResponse(int(HTTPStatus.INTERNAL_SERVER_ERROR),f'Failed to fetch data for symbol {symbol}, Exception: {e}',{})