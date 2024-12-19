from mongoengine import Document, EmbeddedDocument
from mongoengine import StringField, DecimalField, IntField, DateTimeField, BooleanField, EmbeddedDocumentField, DictField
from datetime import datetime,timezone

COLLECTION='stock-backend-collection'

class Fundamentals(EmbeddedDocument):
    pe_ratio=DecimalField(max_digits=15, decimal_places=2)
    eps=DecimalField(max_digits=15, decimal_places=2)
    revenue=DecimalField(max_digits=15, decimal_places=2)
    net_income=DecimalField(max_digits=15, decimal_places=2)
    dividend_yield=DecimalField(max_digits=15, decimal_places=2)
    def to_dict(self):
        return {
            'pe_ratio': self.pe_ratio if self.pe_ratio else None,
            'eps': self.eps if self.eps else None,
            'revenue': self.revenue if self.revenue else None,
            'net_income': self.net_income if self.net_income else None,
            'dividend_yield': self.dividend_yield if self.dividend_yield else None,
        }

class Stock(Document):
    symbol=StringField(max_length=20,required=True,unique=True)
    company=StringField(max_length=200)
    industry=StringField(max_length=200)
    sector=StringField(max_length=200)
    country=StringField(max_length=50)
    currency=StringField(max_length=50)
    market_cap=IntField()
    shares_outstanding=IntField()
    fundamentals=EmbeddedDocumentField(Fundamentals)
    technicals=DictField()
    provider=StringField(max_length=20)
    found=BooleanField(default=False)
    meta={
        'collection':COLLECTION,
        'indexes':[
            {'fields':['symbol'],'unique':True},
        ]
    }
    def to_dict(self):
        return {
            'symbol': self.symbol,
            'company': self.company if self.company else None,
            'industry': self.industry if self.industry else None,
            'sector': self.sector if self.sector else None,
            'country': self.country if self.country else None,
            'currency': self.currency if self.currency else None,
            'market_cap': self.market_cap if self.market_cap else None,
            'shares_outstanding': self.shares_outstanding if self.shares_outstanding else None,
            'fundamentals': self.fundamentals.to_dict() if self.fundamentals else None,
            'technicals': self.technicals or None,
            'provider': self.provider if self.provider else None,
            'found': self.found,
        }
    @classmethod
    def upsert_stock(cls,stock):
        return cls.objects(symbol=stock.symbol).modify(
            upsert=True,
            new=True,
            set__company=stock.company,
            set__industry=stock.industry,
            set__sector=stock.sector,
            set__country=stock.country,
            set__currency=stock.currency,
            set__market_cap=stock.market_cap,
            set__shares_outstanding=stock.shares_outstanding,
            set__fundamentals=stock.fundamentals,
            set__technicals=stock.technicals,
            set__provider=stock.provider,
            set__found=stock.found,
        )

class Forex(Document):
    symbol=StringField(max_length=20,required=True,unique=True)
    base_currency=StringField(max_length=20,required=True)
    quote_currency=StringField(max_length=20,required=True)
    exchange=StringField(max_length=20,required=True)
    name=StringField(max_length=20)
    provider=StringField(max_length=20)
    found=BooleanField(default=False)
    meta={
        'collection':COLLECTION,
        'indexes':[
            {'fields':['symbol'],'unique':True},
        ]
    }
    def to_dict(self):
        return {
            'symbol': self.symbol,
            'base_currency': self.base_currency if self.base_currency else None,
            'quote_currency': self.quote_currency if self.quote_currency else None,
            'exchange': self.exchange if self.exchange else None,
            'name': self.name if self.name else None,
            'provider': self.provider if self.provider else None,
            'found': self.found,
        }
    @classmethod
    def upsert_forex(cls,forex):
        return cls.objects(symbol=forex.symbol).modify(
            upsert=True,
            new=True,
            set__base_currency=forex.base_currency,
            set__quote_currency=forex.quote_currency,
            set__exchange=forex.exchange,
            set__name=forex.name,
            set__provider=forex.provider,
            set__found=forex.found,
        )

class Cryptocurrency(Document):
    symbol=StringField(max_length=20,required=True,unique=True)
    name=StringField(max_length=20)
    provider=StringField(max_length=20)
    found=BooleanField(default=False)
    meta={
        'collection':COLLECTION,
        'indexes':[
            {'fields':['symbol'],'unique':True},
        ]
    }
    def to_dict(self):
        return {
            'symbol': self.symbol,
            'name': self.name if self.name else None,
            'provider': self.provider if self.provider else None,
            'found': self.found,
        }
    @classmethod
    def upsert_cryptocurrency(cls,cryptocurrency):
        return cls.objects(symbol=cryptocurrency.symbol).modify(
            upsert=True,
            new=True,
            set__name=cryptocurrency.name,
            set__provider=cryptocurrency.provider,
            set__found=cryptocurrency.found,
        )