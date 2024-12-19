import json
from django.shortcuts import render
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.response import Response
from .use_cases.get_stock_data import fetch_stock_data,fetch_market_exchange_data,fetch_all_symbols_from_market,fmp_contains,eod_contains
from .interfaces.mongodb_handler import fetch_from_mongo_collection,drop_collections_from_mongo
from .utils import APIResponse, APIResponseRenderer
from .interfaces.mongodb_handler import is_asset_in_mongo
from bson import ObjectId
from .tasks import async_market_population
from django.http import JsonResponse
from .domain.models import Stock

api_url='https://localhost/stocks'

@api_view(['GET'])
@renderer_classes([APIResponseRenderer])
def get_stock_data(request,symbol):
    """Takes in stock symbol and produces a dictionary with the information
    in the StockData class, also saving to the database"""
    try:
        response_code=404
        #api=fetch_stock_data_fmp if fmp_contains(symbol) else fetch_stock_data_eodhd
        #provider='FMP' if fmp_contains(symbol) else 'EOD'
        provider='None'
        #if is_asset_in_mongo(symbol):
        if True:
            print('found api function')
            response_code,stock=fetch_stock_data(symbol,provider)

            if response_code==200 and stock is not None:
                msg='Data retrieved successfully'
                print('making api response')
                api_response=APIResponse(response_code,msg,stock.to_dict())
                return JsonResponse(api_response.to_dict())

        failure_response=APIResponse(404,f'Data not retrieved for symbol {symbol}', None)
        return JsonResponse(failure_response.to_dict())
    except Exception as e:
        error_response=APIResponse(500, f'Internal server error: {str(e)}', None)
        return JsonResponse(error_response.to_dict())

@api_view(['GET'])
def get_multi_stock_data(request,symbols):
    list_of_symbols=symbols.split(',')
    result=[]
    for symbol in list_of_symbols:
        response_code,stock_data=get_stock_data(request,symbol)
        #result.append
    return Response(result)

@api_view(['GET'])
def get_fundamentals(request):
    pass

#@api_view(['GET'])
def get_assets_under_market(market_ticker):
    pass

@api_view(['GET'])
def get_market_exchange_data(request):
    async_market_population.delay()
    market_exchange_data=APIResponse(200,'Begun populating database with market data..',None)
    return JsonResponse(market_exchange_data.to_dict())

@api_view(['DELETE'])
def clear_test_collections(request):
    # This is just for testing purposes obviously, will not be in the real thing
    drop_collections_from_mongo()
    return Response('Deleted collections')
