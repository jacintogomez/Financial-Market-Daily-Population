from decouple import config
import requests
from http import HTTPStatus
import re
from requests import RequestException
from ...apiresponse.model.models import APIResponse
from ...apiresponse.controller.fetch_data import form_response_symbol,form_response,check_for_problems

fmp_api_suffix='apikey='+config('FMP_API_KEY')
fmp_api_prefix='https://financialmodelingprep.com/api/'

symbol_specific_url_mapping={
    'v3/earnings_calendar':'earnings-calendar',
    'v3/historical/earning_calendar':'earnings-historical',
    'v3/earnings-surprises':'earnings-surprises',
}

single_urls=[
    'v4/earning-calendar-confirmed',
]

def fetch_symbol_specific_earnings_data(symbol):
    if not symbol:
        return APIResponse(int(HTTPStatus.BAD_REQUEST),{},'No symbol provided')
    earnings_data={
        'earnings-calendar':{},
        'earnings-historical':{},
        'earnings-surprises':{},
    }
    def make_request(url):
        full_url=f'{fmp_api_prefix}{url}/{symbol}?{fmp_api_suffix}'
        print('full_url=',full_url)
        try:
            return check_for_problems(full_url,url,symbol)
        except requests.exceptions.HTTPError as e:
            return False,f'HTTP error {e} occurred from {url}',None
        except RequestException as e:
            return False,f'Request exception {e} occurred from {url}',None
    try:
        successes=0
        total_endpoints=len(symbol_specific_url_mapping)
        errors=[]
        for url in symbol_specific_url_mapping:
            endpoint_key=symbol_specific_url_mapping[url]
            print('name is ',endpoint_key)
            status,error,data=make_request(url)
            print('status is ',status)
            if status:
                earnings_data[endpoint_key]=data
                successes+=1
            else:
                errors.append(error)
        apiresponse=form_response_symbol(successes,symbol,'Earnings',earnings_data,total_endpoints,errors)
        return apiresponse
    except Exception as e:
        return APIResponse(int(HTTPStatus.INTERNAL_SERVER_ERROR),f'Failed to fetch data for symbol {symbol}, Exception: {e}',{})

def fetch_singular_earnings_data():
    earnings_data={}
    def make_request(url):
        full_url=f'{fmp_api_prefix}{url}?{fmp_api_suffix}'
        print('full_url=',full_url)
        try:
            return check_for_problems(full_url,url)
        except requests.exceptions.HTTPError as e:
            return False,f'HTTP error {e} occurred from {url}',None
        except RequestException as e:
            return False,f'Request exception {e} occurred from {url}',None
    try:
        successes=0
        total_endpoints=len(single_urls)
        errors=[]
        for url in single_urls:
            endpoint_key='earning-calendar-confirmed'
            print('name is ',endpoint_key)
            status,error,data=make_request(url)
            print('status is ',status)
            if status:
                earnings_data[endpoint_key]=data
                successes+=1
            else:
                errors.append(error)
        apiresponse=form_response(successes,'Earnings',earnings_data,total_endpoints,errors)
        return apiresponse
    except Exception as e:
        return APIResponse(int(HTTPStatus.INTERNAL_SERVER_ERROR),f'Failed to fetch data for Earnings Calendar Confirmed, Exception: {e}',{})