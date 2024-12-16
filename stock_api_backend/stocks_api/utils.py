from datetime import datetime, timezone
from typing import Generic, Optional, TypeVar
from rest_framework.renderers import JSONRenderer
from django.http import HttpResponse
import json

T=TypeVar('T')

class APIResponseRenderer(JSONRenderer):
    def render(self,data,accepted_media_type=None,renderer_context=None):
        if hasattr(data,'to_dict'):
            response_data=data.to_dict()
            json_data=json.dumps(response_data)
            return HttpResponse(content=json_data,content_type='application/json',status=data.status_code)
        return super().render(data,accepted_media_type,renderer_context)

class StockData:
    def __init__(self,ticker):
        self.ticker=ticker
        self.provider=''
        self.price=0
        self.day_high=0
        self.day_low=0
        self.open_price=0
        self.change=0
        self.percent_change=0
        self.volume=0
        self.market_cap=0
        self.pe_ratio=0
        self.dividend_yield=0
        self.found=False
    def __str__(self):
        return f'ticker: {self.ticker}, price: {self.price}'

class FundamentalsData:
    def __init__(self):
        self.parameters=0

class APIResponse:
    def __init__(self,code,message,data=None):
        self.timestamp=datetime.now(timezone.utc).isoformat()
        self.status_code=code
        self.message=message
        self.data=data
    def to_dict(self):
        return {
            'timestamp': self.timestamp,
            'status_code': self.status_code,
            'data': self.data.__dict__,
            'message': self.message,
        }

class ErrorDetails:
    def __init__(self,status,details,field):
        self.status_code=status
        self.details=details
        self.field=field

