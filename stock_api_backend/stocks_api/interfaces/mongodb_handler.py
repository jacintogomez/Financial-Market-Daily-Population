from pymongo import MongoClient
from decouple import config

mongo_uri=config('MONGO_URI')
client=MongoClient(mongo_uri)

db=client['stock-backend']
collection=db['stock-backend-collection']

def save_to_mongo(data):
    #collection.insert_one(data)
    query={'ticker':data['ticker']}
    collection.update_one(query,{'$set':data},upsert=True)

def fetch_from_mongo():
    return list(collection.find({},{'_id':0}))