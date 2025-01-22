from decouple import config
import requests
from http import HTTPStatus
from requests import RequestException
import re
from ...apiresponse.model.models import APIResponse
from ...apiresponse.controller.fetch_data import form_response,check_for_problems

fmp_api_suffix='apikey='+config('FMP_API_KEY')
fmp_api_prefix='https://financialmodelingprep.com/api/'

urls=[
    'v4/crowdfunding-offerings-rss-feed',
]

def fetch_fundraising_data():
    fundraising_data={
        'crowdfunding-offerings-rss-feed':{},
    }
    def make_request(url):
        full_url=f'{fmp_api_prefix}{url}?{fmp_api_suffix}'
        print('full url:', full_url)
        try:
            return check_for_problems(full_url,url)
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
            status,error,data=make_request(url)
            print('status is',status)
            if status:
                fundraising_data[endpoint_key]=data
                successes+=1
            else:
                errors.append(endpoint_key)
        apiresponse=form_response(successes,'Fundraising',fundraising_data,total_endpoints,errors)
        return apiresponse
    except Exception as e:
        return APIResponse(int(HTTPStatus.INTERNAL_SERVER_ERROR),f'Failed to fetch Fundraising data, Exception: {e}',{})