from mongoengine import Document,StringField,DictField,DateTimeField
from datetime import datetime,timezone

class Earnings(Document):
    symbol=StringField(max_length=20,required=True,unique=True)
    earnings_calendar=DictField()
    earnings_historical=DictField()
    earnings_confirmed=DictField()
    earnings_surprises=DictField()
    collection_name='earnings'
    provider=StringField(max_length=20)
    timestamp=DateTimeField(default=datetime.now(timezone.utc).isoformat())
    meta={
        'collection':'earnings',
        'indexes':[
            {'fields':['symbol'],'unique':True},
        ],
        'index_background':True,
    }
    def to_dict(self):
        return {
            'symbol': self.symbol,
            'earnings_calendar': self.earnings_calendar or None,
            'earnings_historical': self.earnings_historical or None,
            'earnings_confirmed': self.earnings_confirmed or None,
            'earnings_surprises': self.earnings_surprises or None,
            'provider': self.provider or None,
        }
    @classmethod
    def upsert_asset(cls,symbol,new_historical,new_surprises):
        return cls.objects(symbol=symbol).modify(
            upsert=True,
            new=True,
            set__earnings_historical=new_historical,
            set__earnings_surprises=new_surprises,
            set__timestamp=datetime.now(timezone.utc).isoformat(),
        )
    @classmethod
    def upsert_single_asset(cls,symbol,new_calendar,new_confirmed):
        return cls.objects(symbol=symbol).modify(
            upsert=True,
            new=True,
            set__earnings_calendar=new_calendar,
            set__earnings_confirmed=new_confirmed,
            set__timestamp=datetime.now(timezone.utc).isoformat(),
        )