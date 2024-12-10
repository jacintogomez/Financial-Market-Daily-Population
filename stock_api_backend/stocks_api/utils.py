from datetime import datetime, timezone
from typing import Generic, Optional, TypeVar

T=TypeVar('T')

class FMPData:
    def __init__(self,data=None):
        self.price=data[0]['Stock Price']
    def to_dict(self):
        return { 'price': self.price if self.price else None }

class EODHDData:
    def __init__(self,data=None):
        self.price=data['close'] if data else None
    def to_dict(self):
        return { 'price': self.price if self.price else None }

class APIResponse:
    def __init__(self,ticker,FMP=None,EODHD=None):
        self.ticker=ticker
        self.timestamp=datetime.now(timezone.utc).isoformat()
        self.FMP=FMP
        self.EODHD=EODHD
    def __str__(self):
        return self.ticker
    def to_dict(self):
        return {
            'ticker': self.ticker,
            'timestamp': self.timestamp,
            'FMP': {
                'price': self.FMP.to_dict() if self.FMP else None
            },
            'EODHD': {
                'price': self.EODHD.to_dict() if self.EODHD else None
            }
        }

class ErrorDetails:
    def __init__(self,status,details,field):
        self.status_code=status
        self.details=details
        self.field=field
