from django.test import TestCase

from .use_cases.get_stock_data import fetch_stock_data_fmp
from .utils import StockData,APIResponse
from unittest.mock import patch

class Tests(TestCase):
    def test_stock_data_initialization(self):
        stock=StockData('AAPL')
        assert stock.ticker=='AAPL'
        assert stock.price==0
        assert stock.convert_data_to_dict()==stock.__dict__

    def test_api_response_creation(self):
        stock_data=StockData('AAPL')
        message='Retrieved data successfully'
        response=APIResponse(200,message,stock_data)
        response_dict=response.to_dict()
        assert response_dict['status_code']==200
        assert response_dict['message']==message

    # def test_fetch_stock_data_fmp_success(self):
    #     with patch('requests.get') as mock_get:
    #         mock_response1=mock_get.return_value
    #         mock_response1.status_code=200
    #         mock_response1.json.return_value=[
    #             {
    #                 'price':150.00,
    #                 'dayHigh':155.00,
    #                 'dayLow':145.00,
    #                 'open':148.00,
    #                 'change':2.00,
    #                 'changesPercentage':1.35,
    #                 'volume':1000000,
    #                 'pe':25.5,
    #             }
    #         ]
    #
    #         status_code,stock_data=fetch_stock_data_fmp('AAPL')
    #         assert stock_data.price==150.00
    #
    #         mock_response2=mock_get.return_value
    #         mock_response2.status_code=200
    #         mock_response2.json.return_value=[
    #             {
    #                 'mktCap':2500000000,
    #                 'lastDiv':0.5,
    #             }
    #         ]
    #
    #         status_code,stock_data=fetch_stock_data_fmp('AAPL')
    #         assert status_code==200
    #         assert stock_data.found==True
    #         assert stock_data.provider=='FMP'
    #         assert stock_data.market_cap==2500000000

    def test_fetch_stock_data_fmp_fail(self):
        with patch('requests.get') as mock_get:
            mock_response1=mock_get.return_value
            mock_response1.status_code=404
            mock_response1.json.return_value=[]

            status_code,stock_data=fetch_stock_data_fmp('AAPL')
            assert status_code==404
            assert stock_data.found==False