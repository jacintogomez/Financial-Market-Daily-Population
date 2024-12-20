from mongoengine import Document
from mongoengine import StringField, DictField

class Fundamentals(Document):
    symbol=StringField(max_length=20,required=True,unique=True)
    data=DictField()
    provider=StringField(max_length=20)
    meta={
        'collection':'fundamentals',
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
    def upsert_asset(cls,symbol,new_data):
        return cls.objects(symbol=symbol).modify(
            upsert=True,
            new=True,
            set__data=new_data,
        )