from ..model.models import APIResponse
from http import HTTPStatus
import requests

def validate_api_response(data):
    if data is None:
        return None
    if isinstance(data,list) or isinstance(data,dict):
        if not data:
            return None
        return data
    return None

def validate_singular_api_response(data):
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

def check_for_problems(full_url,url,symbol=None):
    response=requests.get(full_url)
    if response.status_code==HTTPStatus.NOT_FOUND:
        return False,f'Endpoint {url} not found',None
    response.raise_for_status()
    try:
        data=response.json()
    except requests.exceptions.JSONDecodeError as e:
        return False,f'Invalid JSON response {e} from {url}',None
    validate_data=validate_singular_api_response(data) if symbol else validate_api_response(data)
    if validate_data is not None:
        return True,'',validate_data
    return False,f'No valid data returned from {url}',None

def form_response(successes,category,data,endpoints,errors):
    if successes==0:
        return APIResponse(int(HTTPStatus.SERVICE_UNAVAILABLE),f'Failed to fetch {category} data',{})
    if not data:
        return APIResponse(int(HTTPStatus.NO_CONTENT),f'No valid {category} data received',{})
    if successes<endpoints:
        return APIResponse(int(HTTPStatus.PARTIAL_CONTENT),f'Could not retrieve data for all {category} endpoints: {errors}',data)
    return APIResponse(int(HTTPStatus.OK),f'Successfully retrieved {category} data',data)

def form_response_symbol(successes,symbol,category,data,endpoints,errors):
    if successes==0:
        print('no data collected from api')
        return APIResponse(int(HTTPStatus.SERVICE_UNAVAILABLE),f'Failed to fetch {category} data for symbol {symbol}',{})
    if not data:
        return APIResponse(int(HTTPStatus.NO_CONTENT),f'No valid {category} data received for symbol {symbol}',{})
    if successes<endpoints:
        return APIResponse(int(HTTPStatus.PARTIAL_CONTENT),f'Could not retrieve {category} data for all {symbol} endpoints: {errors}',data)
    return APIResponse(int(HTTPStatus.OK),f'Successfully retrieved {category} data for {symbol}',data)