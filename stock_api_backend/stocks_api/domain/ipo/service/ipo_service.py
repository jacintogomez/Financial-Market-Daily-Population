from decouple import config
import requests
from http import HTTPStatus
import re
from requests import RequestException
from ...apiresponse.model.models import APIResponse

fmp_api_suffix='apikey='+config('FMP_API_KEY')
fmp_api_prefix='https://financialmodelingprep.com/api/'

urls=[
    'v4/ipo-calendar-confirmed',
    'v4/ipo-calendar-prospectus',
    'v3/ipo-calendar',
]

def validate_api_response(data):
    print('validating ipos')
    if data is None:
        return None
    if isinstance(data,list) or isinstance(data,dict):
        if not data:
            return None
        return data
    return None

def fetch_ipo_calendar_data():
    ipo_data={
        'ipo-calendar-confirmed':{},
        'ipo-calendar-prospectus':{},
        'ipo-calendar':{},
    }
    def make_request(url,endpoint):
        full_url=f'{fmp_api_prefix}{url}?{fmp_api_suffix}'
        print('full_url=',full_url)
        try:
            response=requests.get(full_url)
            if response.status_code==HTTPStatus.NOT_FOUND:
                return False,f'Endpoint {url} not found',None
            response.raise_for_status()
            try:
                data=response.json()
            except requests.exceptions.JSONDecodeError as e:
                return False,f'JSON decode error {e} from {url}',None
            validated_data=validate_api_response(data)
            if validated_data is not None:
                return True,'',validated_data
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
            endpoint_key=re.split(r'[/?]',url)[-1]
            print('endpoint key is',endpoint_key)
            status,error,data=make_request(url,endpoint_key)
            print('status is',status)
            if status:
                ipo_data[endpoint_key]=data
                successes+=1
            else:
                errors.append(endpoint_key)
        print('initial ipo data',ipo_data)
        if successes==0:
            print('no ipo data')
            return APIResponse(int(HTTPStatus.SERVICE_UNAVAILABLE),f'Failed to fetch IPO data',{})
        if not ipo_data:
            print('no valid ipo data')
            return APIResponse(int(HTTPStatus.NO_CONTENT),f'No valid IPO data received',{})
        if successes<total_endpoints:
            print('partial data retrieved')
            return APIResponse(int(HTTPStatus.PARTIAL_CONTENT),f'Could not retrieve data for all IPO endpoints: {errors}',ipo_data)
        print('success data retrieved')
        return APIResponse(int(HTTPStatus.OK),f'Successfully retrieved IPO data',ipo_data)
    except Exception as e:
        return APIResponse(int(HTTPStatus.INTERNAL_SERVER_ERROR),f'Failed to fetch IPO data, Exception: {e}',{})