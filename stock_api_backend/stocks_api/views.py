from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import json
from datetime import datetime

from .domain.mergersacquisitions.model.models import Mergers_Acquisitions
from .domain.mergersacquisitions.service.mergers_acquisitions_service import fetch_mergers_acquisitions_data
from .api_access.get_stock_data import fetch_stock_data_from_api
from .api_access.post_stock_data import post_stock_data_to_collection
from .db_access.mongodb_handler import drop_collections_from_mongo,display_all_symbols_from_mongo
from .utils import APIResponse
from .tasks import async_market_population,populate_fmp_stocks
from .domain.fundamentals.service.fundamentals_service import fetch_fundamentals_data
from .domain.fundamentals.model.models import Fundamentals
from .domain.ipo.service.ipo_service import fetch_ipo_calendar_data
from .domain.ipo.model.models import IPO
from .domain.fundraising.model.models import Fundraising
from .domain.fundraising.service.fundraising_service import fetch_fundraising_data
from .domain.esg.model.models import ESG
from .domain.esg.service.esg_service import fetch_esg_data
from .domain.news.model.models import News
from .domain.news.service.news_service import fetch_news_data
from .domain.rating.model.models import Rating
from .domain.rating.service.rating_service import fetch_rating_data
from .domain.earnings.model.models import Earnings
from .domain.earnings.service.earnings_service import fetch_symbol_specific_earnings_data,fetch_singular_earnings_data
from django.http import JsonResponse
from pymongo import MongoClient
from decouple import config

mongo_uri=config('MONGO_URI')
client=MongoClient(mongo_uri)
db=client[config('MONGODB_DB_NAME')]
assets_collection=db['market_symbols']
fmp_assets_collection=db['market_fmp_symbols']

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
    fundamentals_response=0
    for symb in cursor[:3]:
        symbol=symb['Code']
        print(symbol)
        fundamentals_response=fetch_fundamentals_data(symbol)
        print('got obj')
        fundamentals=Fundamentals(symbol=symbol,provider='EOD')
        if fundamentals_response.status_code==200:
            fundamentals.upsert_asset(symbol,fundamentals_response.data)
    return JsonResponse(fundamentals_response.to_dict())

@api_view(['POST'])
def update_esg(request):
    cursor=fmp_assets_collection.find(batch_size=100)
    esg_response=0
    for symb in cursor[:3]:
        symbol=symb['symbol']
        print(symbol)
        esg_response=fetch_esg_data(symbol)
        print('got obj')
        esg=ESG(symbol=symbol,provider='FMP')
        if esg_response.status_code==200:
            esg.upsert_asset(symbol,esg_response.data)
    return JsonResponse(esg_response.to_dict())

@api_view(['POST'])
def update_news(request):
    cursor=assets_collection.find(batch_size=100)
    news_response=0
    for symb in cursor[:3]:
        symbol=symb['Code']
        market=symb['Exchange']
        print(symbol)
        news_response=fetch_news_data(symbol,market)
        print('got obj')
        news=News(symbol=symbol,provider='EOD')
        if news_response.status_code==200:
            news.upsert_asset(symbol,news_response.data)
    return JsonResponse(news_response.to_dict())

@api_view(['POST'])
def update_rating(request):
    cursor=fmp_assets_collection.find(batch_size=100)
    rating_response=0
    for symb in cursor[:3]:
        symbol=symb['symbol']
        print(symbol)
        rating_response=fetch_rating_data(symbol)
        print('got obj')
        rating=Rating(symbol=symbol,provider='FMP')
        if rating_response.status_code==200:
            rating.upsert_asset(symbol,rating_response.data)
    return JsonResponse(rating_response.to_dict())

@api_view(['POST'])
def update_earnings(request):
    earnings_cc=Earnings(symbol='Earnings',provider='FMP')
    earnings_cc_response=fetch_singular_earnings_data()
    if earnings_cc_response.status_code in [200,206]:
        earnings_cc.upsert_single_asset('Earnings Calendar Confirmed',earnings_cc_response.data)
    cursor=fmp_assets_collection.find(batch_size=100)
    earnings_response=0
    for symb in cursor:
        symbol=symb['symbol']
        print(symbol)
        earnings_response=fetch_symbol_specific_earnings_data(symbol)
        print('got obj')
        earnings=Earnings(symbol=symbol,provider='FMP')
        if earnings_response.status_code in [200,206]:
            earnings.upsert_asset(symbol,earnings_response.data['earnings-calendar'],earnings_response.data['earnings-historical'],earnings_response.data['earnings-surprises'])
        else:
            print('invalid response',earnings_response.status_code)
    return JsonResponse(earnings_response.to_dict())

@api_view(['POST'])
def update_fundraising(request):
    fundraising_response=fetch_fundraising_data()
    fundraising=Fundraising(symbol='Fundraising',provider='FMP')
    if fundraising_response.status_code==200 or fundraising_response.status_code==206:
        print('upserting fundraising')
        print(fundraising_response.to_dict())
        fundraising.upsert_asset('Fundraising',fundraising_response.data['crowdfunding-offerings-rss-feed'])
    return JsonResponse(fundraising_response.to_dict())

@api_view(['POST'])
def update_mergers_acquisitions(request):
    mergers_acquisitions_response=fetch_mergers_acquisitions_data()
    mergers_acquisitions=Mergers_Acquisitions(symbol='Mergers & Acquisitions',provider='FMP')
    if mergers_acquisitions_response.status_code==200 or mergers_acquisitions_response.status_code==206:
        print('upserting mergers & acquisitions')
        print(mergers_acquisitions_response.to_dict())
        mergers_acquisitions.upsert_asset('Mergers & Acquisitions',mergers_acquisitions_response.data['mergers-acquisitions-rss-feed'])
    return JsonResponse(mergers_acquisitions_response.to_dict())

@api_view(['GET'])
def get_market_exchange_data(request):
    async_market_population.delay()
    market_exchange_data=APIResponse(200,'Begun populating database with market data..',None)
    return JsonResponse(market_exchange_data.to_dict())

@api_view(['GET'])
def get_fmp_symbols_data(request):
    populate_fmp_stocks.delay()
    market_exchange_data=APIResponse(200,'Begun populating database with FMP market data..',None)
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

@api_view(['GET'])
def get_info(request,collection_name,field_path,query_value=None):
    try:
        collection=db[collection_name]
        filters={'symbol':query_value} if query_value else{}
        startdate=request.GET.get('start_date')
        enddate=request.GET.get('end_date')
        datetype=request.GET.get('date_type')
        if (startdate and enddate) and not datetype:
            return JsonResponse({'error':'date_type is required when using date filtering; there are several types of date parameters'},status=400)
        field_keys=field_path.split('-')
        print('field keys:',field_keys)
        mongo_fields='.'.join(field_keys)
        print('mongo fields: ',mongo_fields)
        print('filters: ',filters)
        result=collection.find_one(filters,{mongo_fields:1,'_id':0})
        if result:
            value=result
            for key in field_keys:
                print('key is',key)
                if value and isinstance(value,dict):
                    print('isdict')
                    value=value.get(key,None)
                # elif value and isinstance(value,list):
                #     print('islist')
                #     value=[item for item in value if startdate and enddate and datetime.strptime(item.get(datetype),'%Y-%m-%d')>=datetime.strptime(startdate,'%Y-%m-%d') and datetime.strptime(item.get(datetype),'%Y-%m-%d')<=datetime.strptime(enddate,'%Y-%m-%d')]
                else:
                    print('else')
                    value=None
                    break
            if isinstance(value,list) and startdate and enddate:
                print('islist')
                value=[item for item in value if startdate and enddate and datetime.strptime(item.get(datetype)[:10],'%Y-%m-%d')>=datetime.strptime(startdate,'%Y-%m-%d') and datetime.strptime(item.get(datetype)[:10],'%Y-%m-%d')<=datetime.strptime(enddate,'%Y-%m-%d')]
            return JsonResponse({'data':value},status=200)
        else:
            return JsonResponse({'error':'No matching record found'},status=404)
    except Exception as e:
        print('an exception occurred:',e)
        return JsonResponse({'error':str(e)},status=500)