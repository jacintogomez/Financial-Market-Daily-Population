import json
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .use_cases.get_stock_data import fetch_stock_data_fmp,fetch_stock_data_eodhd
from .interfaces.mongodb_handler import save_to_mongo,fetch_from_mongo
from .utils import StockData,FMPData,EODHDData
from bson import ObjectId

api_url='https://localhost/stocks'

@api_view(['GET'])
def get_stock_data(request,symbol):

    # TODO change the below line to accept all APIs
    fmp_data=FMPData(fetch_stock_data_fmp(symbol))
    eod_data=EODHDData(fetch_stock_data_eodhd(symbol))
    stock_data=StockData(symbol,fmp_data,eod_data)
    print(stock_data.to_dict())
    stocks_dictionary=stock_data.to_dict()

    save_to_mongo(stocks_dictionary)

    # MongoDB specific: need to convert the mandatory _id field from ObjectId to string
    # otherwise there will be an error that ObjectId can't be converted to JSON
    # if '_id' in stock_data.FMP and isinstance(stock_data.FMP['_id'],ObjectId):
    #     stock_data.FMP['_id'] = str(stock_data.FMP['_id'])
    # if '_id' in stock_data.EODHD and isinstance(stock_data.EODHD['_id'],ObjectId):
    #     stock_data.EODHD['_id'] = str(stock_data.EODHD['_id'])
    return Response(stocks_dictionary)

@api_view(['GET'])
def get_all_stocks(request):
    stocks=fetch_from_mongo()
    for stock in stocks:
        if '_id' in stock and isinstance(stock['_id'],ObjectId):
            stock['_id'] = str(stock['_id'])
    return Response(stocks)