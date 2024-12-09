from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .use_cases.get_stock_data import fetch_stock_data_fmp,fetch_stock_data_eodhd
from .interfaces.mongodb_handler import save_to_mongo,fetch_from_mongo
from bson import ObjectId

api_url='https://localhost/stocks'

@api_view(['GET'])
def get_stock_data(request,symbol,provider):
    #below will need to be changed when more API providers are integrated
    stock_data=fetch_stock_data_fmp(symbol) if provider=='fmp' else fetch_stock_data_eodhd(symbol)
    save_to_mongo(stock_data)
    #I need to add the below otherwise it won't recognize the MongoDB objectID field
    if '_id' in stock_data and isinstance(stock_data['_id'],ObjectId):
        stock_data['_id'] = str(stock_data['_id'])
    return Response(stock_data)

@api_view(['GET'])
def get_all_stocks(request):
    stocks=fetch_from_mongo()
    for stock in stocks:
        if '_id' in stock and isinstance(stock['_id'],ObjectId):
            stock['_id'] = str(stock['_id'])
    return Response(stocks)