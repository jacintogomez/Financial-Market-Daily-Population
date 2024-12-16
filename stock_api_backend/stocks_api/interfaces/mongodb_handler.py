from pymongo import MongoClient
from decouple import config

mongo_uri=config('MONGO_URI')
client=MongoClient(mongo_uri)

db=client['stock-backend']

def save_to_mongo(data,market):
    collection=db[market]
    query={'Code':data['Code']}
    # $set:data will only
    # upsert=True will update a record with matching ticker, and if there is no match it will create a new record
    collection.update_one(query,{'$set':data},upsert=True)

def fetch_from_mongo_collection(market):
    # {} is used to find all documents; no filters
    # {'_id':0} ignores the MongoDB mandatory _id field, which is just for db organization and not useful for a user
    return list(db[market].find({},{'_id':0}))