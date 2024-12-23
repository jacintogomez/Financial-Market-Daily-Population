from mongoengine import Document,StringField,DictField,DateTimeField
from datetime import datetime,timezone

class IPO(Document):
    symbol=StringField(max_length=20,required=True,unique=True)
    ipo_confirmed=DictField()
    ipo_prospectus=DictField()
    ipo_calendar=DictField()
    collection_name='ipo'
    provider=StringField(max_length=20)
    timestamp=DateTimeField(default=datetime.now(timezone.utc).isoformat())
    meta={
        'collection':'ipo',
        'indexes':[
            {'fields':['symbol'],'unique':True},
        ],
        'index_background':True,
    }
    def to_dict(self):
        return {
            'symbol': self.symbol,
            'ipo_confirmed': self.ipo_confirmed or None,
            'ipo_prospectus': self.ipo_prospectus or None,
            'provider': self.provider or None,
        }
    @classmethod
    def upsert_asset(cls,symbol,new_confirmed,new_prospectus,new_calendar):
        return cls.objects(symbol=symbol).modify(
            upsert=True,
            new=True,
            set__ipo_confirmed=new_confirmed,
            set__ipo_prospectus=new_prospectus,
            set__ipo_calendar=new_calendar,
            set__timestamp=datetime.now(timezone.utc).isoformat(),
        )