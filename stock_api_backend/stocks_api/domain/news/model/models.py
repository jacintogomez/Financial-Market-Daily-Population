from mongoengine import Document, StringField, DictField, DateTimeField
from datetime import datetime,timezone

class News(Document):
    symbol=StringField(max_length=20,required=True,unique=True)
    data=DictField()
    collection='news'
    provider=StringField(max_length=20)
    timestamp=DateTimeField(default=datetime.now(timezone.utc).isoformat())
    meta={
        'collection':'news',
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
            set__timestamp=datetime.now(timezone.utc).isoformat(),
        )