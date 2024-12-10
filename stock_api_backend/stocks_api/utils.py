from datetime import datetime, timezone
from typing import Generic, Optional, TypeVar

T=TypeVar('T')

class FMPData:
    def __init__(self,data=None):
        self.price=data[0]['Stock Price']

class EODHDData:
    def __init__(self,data=None):
        self.price=data['close']

class StockData:
    def __init__(self,ticker,FMP=None,EODHD=None):
        self.ticker = ticker
        self.FMP=FMP
        self.EODHD=EODHD
    def __str__(self):
        return self.ticker
    def to_dict(self):
        return {
            'ticker': self.ticker,
            'FMP': {
                'price': self.FMP.price if self.FMP else None
            },
            'EODHD': {
                'price': self.EODHD.price if self.EODHD else None
            }
        }

class APIResponse(Generic[T]):
    def __init__(self,timestamp=None,status=200,message='Operation successful',data=None,error=None):
        #TODO make sure format and use of UTC is appropriate
        self.timestamp=timestamp or datetime.now(timezone.utc).isoformat()
        self.status=status
        self.message=message
        self.data=data
        self.error=error

class ErrorDetails:
    def __init__(self,status,details,field):
        self.status_code=status
        self.details=details
        self.field=field
