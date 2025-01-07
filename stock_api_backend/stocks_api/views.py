from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import json
from .use_cases.get_stock_data import fetch_stock_data_from_api
from .use_cases.post_stock_data import post_stock_data_to_collection
from .interfaces.mongodb_handler import drop_collections_from_mongo,display_all_symbols_from_mongo
from .utils import APIResponse
from .tasks import async_market_population
from .domain.fundamentals.service.fundamentals_service import fetch_fundamentals_data
from .domain.fundamentals.model.models import Fundamentals
from .domain.ipo.service.ipo_service import fetch_ipo_calendar_data
from .domain.ipo.model.models import IPO
from .domain.fundraising.model.models import Fundraising
from .domain.fundraising.service.fundraising_service import fetch_fundraising_data
from django.http import JsonResponse
from pymongo import MongoClient
from decouple import config

mongo_uri=config('MONGO_URI')
client=MongoClient(mongo_uri)
db=client[config('MONGODB_DB_NAME')]
assets_collection=db['market_symbols']

@api_view(['GET'])
def get_stock_data(request,symbol):
    try:
        provider='None'
        if True:
            print('found api function')
            response_code,stock=fetch_stock_data_from_api(symbol,provider)

            if response_code==200 and stock is not None:
                msg='Data retrieved successfully'
                api_response=APIResponse(response_code,msg,stock.to_dict())
                return JsonResponse(api_response.to_dict())

        failure_response=APIResponse(404,f'Data not retrieved for symbol {symbol}', None)
        return JsonResponse(failure_response.to_dict())
    except Exception as e:
        error_response=APIResponse(500, f'Internal server error: {str(e)}', None)
        return JsonResponse(error_response.to_dict())

@api_view(['GET'])
def push_to_db_test(request,symbol,provider,collection):
    num,data=fetch_stock_data_from_api(symbol,provider)
    post_stock_data_to_collection(symbol,provider,collection,data)
    dbresp=APIResponse(num,'this is just a test',None)
    return JsonResponse(dbresp.to_dict())

@api_view(['GET'])
def display_all_symbols(request):
    display_all_symbols_from_mongo()
    display=APIResponse(200,'displayed all tickers',None)
    return JsonResponse(display.to_dict())

@api_view(['POST'])
def update_ipo(request):
    msg='none'
    ipo_response=fetch_ipo_calendar_data()
    ipo=IPO(symbol='IPO Calendar',provider='FMP')
    if ipo_response.status_code==200 or ipo_response.status_code==206:
        print('upserting ipos')
        print(ipo_response.to_dict())
        ipo.upsert_asset('IPO Calendar',ipo_response.data['ipo-calendar-confirmed'],ipo_response.data['ipo-calendar-prospectus'],ipo_response.data['ipo-calendar'])
    return JsonResponse(ipo_response.to_dict())

@api_view(['POST'])
def update_fundamentals(request):
    cursor=assets_collection.find(batch_size=100)
    msg='none'
    fundamentals_response=0
    for symb in cursor:
        symbol=symb['Code']
        print(symbol)
        fundamentals_response=fetch_fundamentals_data(symbol)
        print('got obj')
        fundamentals=Fundamentals(symbol=symbol,provider='EOD')
        if fundamentals_response.status_code==200:
            fundamentals.upsert_asset(symbol,fundamentals_response.data)
    print('returning from ipo data collection')
    return JsonResponse(fundamentals_response.to_dict())

@api_view(['POST'])
def update_fundraising(request):
    fundraising_response=fetch_fundraising_data()
    fundraising=Fundraising(symbol='Fundraising',provider='FMP')
    if fundraising_response.status_code==200 or fundraising_response.status_code==206:
        print('upserting ipos')
        print(fundraising_response.to_dict())
        fundraising.upsert_asset()
    return JsonResponse(fundraising_response.to_dict())

@api_view(['GET'])
def get_market_exchange_data(request):
    async_market_population.delay()
    market_exchange_data=APIResponse(200,'Begun populating database with market data..',None)
    return JsonResponse(market_exchange_data.to_dict())

@api_view(['DELETE'])
def clear_test_collections(request):
    # This is just for testing purposes, will not be in the real thing
    drop_collections_from_mongo()
    return Response('Deleted collections')

#Standard webhook receiver template for testing Ngrok
@csrf_exempt
def webhook_receiver(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print(data)
            # Handle the webhook data here
            print(f"Received webhook: {data}")

            # You could store this in your database
            if data['status'] == 'success':
                # Handle successful task completion
                task_id = data['task_id']
                result = data['result']
                # Do something with the result...
            else:
                # Handle task failure
                error = data['error']
                # Handle the error...

            return HttpResponse(status=200)
        except json.JSONDecodeError:
            return HttpResponse(status=400)
    return HttpResponse(status=405)