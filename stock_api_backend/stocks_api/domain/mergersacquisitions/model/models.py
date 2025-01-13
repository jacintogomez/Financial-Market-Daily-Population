from mongoengine import Document,StringField,DictField,DateTimeField
from datetime import datetime,timezone

class Mergers_Acquisitions(Document):
    symbol=StringField(max_length=20,required=True,unique=True)
    mergers_acquisitions=DictField()
    collection_name='mergers_acquisitions'
    provider=StringField(max_length=20)
    timestamp=DateTimeField(default=datetime.now(timezone.utc).isoformat())
    meta={
        'collection':'mergers_acquisitions',
        'indexes':[
            {'fields':['symbol'],'unique':True},
        ],
        'index_background':True,
    }
    def to_dict(self):
        return {
            'symbol':self.symbol,
            'mergers_acquisitions':self.mergers_acquisitions or None,
            'provider':self.provider or None,
        }
    @classmethod
    def upsert_asset(cls,symbol,new_mergers_acquisitions):
        return cls.objects(symbol=symbol).modify(
            upsert=True,
            new=True,
            set__mergers_acquisitions=new_mergers_acquisitions,
            set__timestamp=datetime.now(timezone.utc).isoformat(),
        )