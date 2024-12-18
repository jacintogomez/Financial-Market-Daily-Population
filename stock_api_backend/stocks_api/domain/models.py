from mongoengine import Document, StringField, DecimalField, IntField, DateTimeField, BooleanField
from datetime import datetime,timezone

class Stock(Document):
    symbol=StringField(max_length=20,required=True,unique=True)
    provider=StringField(max_length=20,required=False)
    price=DecimalField(precision=2)
    day_high=DecimalField(precision=2)
    day_low=DecimalField(precision=2)
    open_price=DecimalField(precision=2)
    change=DecimalField(precision=2)
    percent_change=DecimalField(precision=2)
    volume=IntField()
    market_cap=IntField()
    pe_ratio=DecimalField(precision=2)
    dividend_yield=DecimalField(precision=2)
    found=BooleanField(default=False)
    timestamp=DateTimeField(default=datetime.now(timezone.utc).isoformat())

    meta = {
        'collection': 'stock-backend-collection',
        'indexes':[
            {'fields':['symbol'],'unique':True},
        ]
    }

    def to_dict(self):
        return {
            'symbol': self.symbol,
            'provider': self.provider,
            'price': float(self.price) if self.price else 0,
            'day_high': float(self.day_high) if self.day_high else 0,
            'day_low': float(self.day_low) if self.day_low else 0,
            'open_price': float(self.open_price) if self.open_price else 0,
            'change': float(self.change) if self.change else 0,
            'percent_change': float(self.percent_change) if self.percent_change else 0,
            'volume': self.volume,
            'market_cap': self.market_cap,
            'pe_ratio': float(self.pe_ratio) if self.pe_ratio else 0,
            'dividend_yield': float(self.dividend_yield) if self.dividend_yield else 0,
            'found': self.found,
            'timestamp': self.timestamp if self.timestamp else None
        }

    @classmethod
    def upsert_stock(cls,stock):
        return cls.objects(symbol=stock.symbol).modify(
            upsert=True,
            new=True,
            set__provider=stock.provider,
            set__price=stock.price,
            set__day_high=stock.day_high,
            set__day_low=stock.day_low,
            set__open_price=stock.open_price,
            set__change=stock.change,
            set__percent_change=stock.percent_change,
            set__volume=stock.volume,
            set__market_cap=stock.market_cap,
            set__pe_ratio=stock.pe_ratio,
            set__dividend_yield=stock.dividend_yield,
            set__found=stock.found,
            set__timestamp=datetime.now(timezone.utc).isoformat()
        )