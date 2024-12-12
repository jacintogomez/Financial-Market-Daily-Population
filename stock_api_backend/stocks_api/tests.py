from django.test import TestCase
from .utils import StockData,APIResponse
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

    def test_fetch_stock_data_fmp_success(self):
        pass

    def test_fetch_stock_data_fmp_fail(self):
        pass