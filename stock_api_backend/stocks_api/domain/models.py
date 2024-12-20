from mongoengine import Document, EmbeddedDocument
from mongoengine import StringField, DecimalField, IntField, DateTimeField, BooleanField, EmbeddedDocumentField, DictField
from datetime import datetime,timezone

COLLECTION='fundamentals-backend-collection'

class Asset(Document):
    symbol=StringField(max_length=20,required=True,unique=True)
    collection=StringField(max_length=20,required=True)
    data=DictField()
    provider=StringField(max_length=20)
    meta={
        'indexes':[
            {'fields':['symbol'],'unique':True},
        ],
        'index_background':True,
    }
    def to_dict(self):
        return {
            'symbol': self.symbol,
            'data': self.data or None,
            'provider': self.provider or None,
        }
    @classmethod
    def upsert_asset(cls,symbol,newdata,collection):
        db=cls._get_db()
        collection=db[collection]
        collection.update_one(
            {'symbol':symbol},
            {'$set':{'data':newdata}},
            upsert=True,
        )
        return collection.find_one({'symbol':symbol})