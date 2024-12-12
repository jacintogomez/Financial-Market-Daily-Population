from datetime import datetime, timezone
from typing import Generic, Optional, TypeVar

T=TypeVar('T')

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
    def __str__(self):
        return f'ticker: {self.ticker}, price: {self.price}'
    def convert_data_to_dict(self):
        return self.__dict__

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
            'data': self.data.convert_data_to_dict(),
            'message': self.message,
        }

class ErrorDetails:
    def __init__(self,status,details,field):
        self.status_code=status
        self.details=details
        self.field=field
