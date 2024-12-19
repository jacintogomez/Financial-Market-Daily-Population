from mongoengine import Document, EmbeddedDocument
from mongoengine import StringField, DecimalField, IntField, DateTimeField, BooleanField, EmbeddedDocumentField, DictField
from datetime import datetime,timezone

COLLECTION='stock-backend-collection'

class Stock(Document):
    symbol=StringField(max_length=20,required=True,unique=True)
    data=DictField()
    provider=StringField(max_length=20)
    meta={
        'collection':COLLECTION,
        'indexes':[
            {'fields':['symbol'],'unique':True},
        ]
    }
    def to_dict(self):
        return {
            'symbol': self.symbol,
            'data': self.data or None,
            'provider': self.provider or None,
        }
    @classmethod
    def upsert_stock(cls,symbol,new_data):
        return cls.objects(symbol=symbol).modify(
            upsert=True,
            new=True,
            set__data=new_data,
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