from pymongo import MongoClient
from decouple import config

mongo_uri=config('MONGO_URI')
client=MongoClient(mongo_uri)

db=client['stock-backend']
collection=db['stock-backend-collection']

def save_to_mongo(data):
    # collection.insert_one(data)
    query={'ticker':data['ticker']} #TODO This should probably use datetime as another primary key
    # $set:data will only
    # upsert=True will update a record with matching ticker, and if there is no match it will create a new record
    collection.update_one(query,{'$set':data},upsert=True)

def fetch_from_mongo():
    # {} is used to find all documents; no filters
    # {'_id':0} ignores the MongoDB mandatory _id field, which is just for db organization and not useful for a user
    return list(collection.find({},{'_id':0}))