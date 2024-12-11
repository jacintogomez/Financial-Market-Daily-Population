import json
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .use_cases.get_stock_data import fetch_stock_data_fmp,fetch_stock_data_eodhd
from .interfaces.mongodb_handler import save_to_mongo,fetch_from_mongo
from .utils import APIResponse
from bson import ObjectId

api_url='https://localhost/stocks'
api_functions=[fetch_stock_data_fmp]

@api_view(['GET'])
def get_stock_data(request,symbol):
    """Takes in stock symbol and produces a dictionary with the information
    in the StockData class, also saving to the database"""
    # TODO change the below line to accept all APIs

    # Iterate over every API option to find the stock data
    # Once it is found on a provider API, stop and return those results
    for api in api_functions:
        response_code,retrieved_data,api_provider=api(symbol)
        if response_code==200 and retrieved_data is not None:
            stock_data=APIResponse(api_provider,retrieved_data)
            print(stock_data.to_dict())
            stocks_dictionary=stock_data.to_dict()

            save_to_mongo(stocks_dictionary)
            return Response(stocks_dictionary)

    # If the stock is not retrievable by any API (or doesn't exist)
    return Response({'message':'Stock Data Not Found'})

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