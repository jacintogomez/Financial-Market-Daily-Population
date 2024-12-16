import json
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .use_cases.get_stock_data import fetch_stock_data_fmp,fetch_stock_data_eodhd,fetch_market_exchange_data,fetch_all_symbols_from_market
from .interfaces.mongodb_handler import save_to_mongo,fetch_from_mongo_collection,drop_collections_from_mongo
from .utils import APIResponse
from bson import ObjectId

api_url='https://localhost/stocks'
api_functions=[fetch_stock_data_fmp]

@api_view(['GET'])
def get_stock_data(request,symbol):
    """Takes in stock symbol and produces a dictionary with the information
    in the StockData class, also saving to the database"""

    # Iterate over every API option to find the stock data
    # Once it is found on a provider API, stop and return those results
    try:
        response_code=200
        for api in api_functions:
            response_code,stock_data=api(symbol)
            if response_code==200 and stock_data is not None:
                if stock_data.found:
                    msg='Data retrieved successfully'
                else:
                    msg='No data retrieved for symbol '+symbol
                api_response=APIResponse(response_code,msg,stock_data)
                api_dictionary=api_response.to_dict()
                return Response(api_dictionary)

        # If the stock is not retrievable by any API (or doesn't exist)
        failure_response=APIResponse(response_code,f'Data not retrieved for symbol {symbol}',None)
        return Response(failure_response.to_dict())
    except Exception as e:
        error_response=APIResponse(500,f'Internal server error: {str(e)}',None)
        return Response(error_response.to_dict())

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
    symbols=fetch_all_symbols_from_market(market_ticker)
    limit=0
    for symbol in symbols[1]:
        limit+=1
        if limit>3:
            break
        save_to_mongo(symbol,market_ticker)

@api_view(['GET'])
def get_market_exchange_data(request):
    code,markets=fetch_market_exchange_data()
    message='Market exchange data retrieved successfully' if code==200 else 'Market exchange data not retrieved'
    market_response=APIResponse(code,message,markets[0])
    limit=0
    for market in markets:
        limit+=1
        if limit>3:
            break
        get_assets_under_market(market['Code'])
    return Response('Added all markets on exchange')

@api_view(['DELETE'])
def clear_test_collections(request):
    # This is just for testing purposes obviously, will not be in the real thing
    drop_collections_from_mongo()
    return Response('Deleted collections')
