from mongoengine import Document,StringField,DictField,DateTimeField
from datetime import datetime,timezone

class Fundraising(Document):
    symbol=StringField(max_length=20,required=True,unique=True)
    crowdfunding_rss=DictField()
    collection_name='fundraising'
    provider=StringField(max_length=20)
    timestamp=DateTimeField(default=datetime.now(timezone.utc).isoformat())
    meta={
        'collection':'fundraising',
        'indexes':[
            {'fields':['symbol'],'unique':True},
        ],
        'index_background':True,
    }
    def to_dict(self):
        return {
            'symbol':self.symbol,
            'crowdfunding_rss':self.crowdfunding_rss or None,
            'provider':self.provider or None,
        }
    @classmethod
    def upsert_asset(cls,symbol,new_crowdfunding_rss):
        return cls.objects(symbol=symbol).modify(
            upsert=True,
            new=True,
            set__crowdfunding_rss=new_crowdfunding_rss,
            set__timestamp=datetime.now(timezone.utc).isoformat(),
        )