from datetime import datetime, timezone
from typing import Generic, Optional, TypeVar

T=TypeVar('T')

class StockData:
    def __init__(self,ticker):
        self.ticker=ticker
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

class APIResponse:
    def __init__(self,ticker,provider=None,data=None):
        self.ticker=ticker
        self.timestamp=datetime.now(timezone.utc).isoformat()
        self.provider=provider
        self.data=data
    def __str__(self):
        return self.ticker
    def to_dict(self):
        return {
            'ticker': self.ticker,
            'timestamp': self.timestamp,
            'provider': self.provider,
            'data': {
                'price': self.data.price if self.data else None,
                'day_high': self.data.day_high if self.data else None,
                'day_low': self.data.day_low if self.data else None,
                'open_price': self.data.open_price if self.data else None,
                'change': self.data.change if self.data else None,
                'percent_change': self.data.percent_change if self.data else None,
                'volume': self.data.volume if self.data else None,
                'market_cap': self.data.market_cap if self.data else None,
                'pe_ratio': self.data.pe_ratio if self.data else None,
                'dividend_yield': self.data.dividend_yield if self.data else None,
            },
        }

class ErrorDetails:
    def __init__(self,status,details,field):
        self.status_code=status
        self.details=details
        self.field=field
