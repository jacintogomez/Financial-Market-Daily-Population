import json
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .use_cases.get_stock_data import fetch_stock_data_fmp,fetch_stock_data_eodhd
from .interfaces.mongodb_handler import save_to_mongo,fetch_from_mongo
from .utils import APIResponse,FMPData,EODHDData
from bson import ObjectId

api_url='https://localhost/stocks'

@api_view(['GET'])
def get_stock_data(request,symbol):

    # TODO change the below line to accept all APIs
    fmp_response_code,fmp_response=fetch_stock_data_fmp(symbol)
    eod_response_code,eod_response=fetch_stock_data_eodhd(symbol)

    fmp_data=FMPData(fmp_response) if (fmp_response_code==200 and fmp_response!=None) else None
    eod_data=EODHDData(eod_response) if (eod_response_code==200 and eod_response!=None) else None
    stock_data=APIResponse(symbol,fmp_data,eod_data)
    print(stock_data.to_dict())
    stocks_dictionary=stock_data.to_dict()

    save_to_mongo(stocks_dictionary)
    return Response(stocks_dictionary)

@api_view(['GET'])
def get_all_stocks(request):
    stocks=fetch_from_mongo()
    for stock in stocks:
        # MongoDB specific: need to convert the mandatory _id field from ObjectId to string
        # otherwise there will be an error that ObjectId can't be converted to JSON
        if '_id' in stock and isinstance(stock['_id'],ObjectId):
            stock['_id'] = str(stock['_id'])
    return Response(stocks)