import json
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .use_cases.get_stock_data import fetch_stock_data_fmp,fetch_stock_data_eodhd,fetch_market_exchange_data,fetch_all_symbols_from_market
from .interfaces.mongodb_handler import save_to_mongo,fetch_from_mongo
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

            #save_to_mongo(stocks_dictionary)
            return Response(api_dictionary)

    # If the stock is not retrievable by any API (or doesn't exist)
    failure_response=APIResponse(response_code,'Data not retrieved',None)
    return Response(failure_response.to_dict())

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

@api_view(['GET'])
def get_all_stocks(request):
    """Returns a list of all stocks in the database"""
    stocks=fetch_from_mongo()
    for stock in stocks:
        # MongoDB specific: need to convert the mandatory _id field from ObjectId to string
        # otherwise there will be an error that ObjectId can't be converted to JSON
        if '_id' in stock and isinstance(stock['_id'],ObjectId):
            stock['_id'] = str(stock['_id'])
    return Response(stocks)

@api_view(['GET'])
def get_assets_under_market(request,market_ticker):
    symbols=fetch_all_symbols_from_market(market_ticker)
    for symbol in symbols[1]:
        save_to_mongo(symbol)
    return Response(symbols)

@api_view(['GET'])
def get_market_exchange_data(request):
    markets=fetch_market_exchange_data()
    for market in markets[1]:
        save_to_mongo(market)
    return Response(markets)
