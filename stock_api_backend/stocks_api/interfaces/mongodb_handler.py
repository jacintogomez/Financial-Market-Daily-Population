from django.http import JsonResponse
from pymongo import MongoClient
from decouple import config
from rest_framework.response import Response
from ..utils import APIResponse

mongo_uri=config('MONGO_URI')
client=MongoClient(mongo_uri)

db=client['stock-backend']

def save_to_mongo(data,market):
    collection=db[market]
    query={'Code':data['Code']}
    # $set:data will only
    # upsert=True will update a record with matching ticker, and if there is no match it will create a new record
    collection.update_one(query,{'$set':data},upsert=True)
    response=APIResponse(200,f'Saved market code {data["Code"]} to MongoDB',None)
    return JsonResponse(response.to_dict())

def fetch_from_mongo_collection(market):
    # {} is used to find all documents; no filters
    # {'_id':0} ignores the MongoDB mandatory _id field
    return list(db[market].find({},{'_id':0}))

def drop_collections_from_mongo():
    # This is just for testing purposes obviously, will not be in the real thing
    deletions=[]
    collections=['US','TO','LSE']
    for collection in collections:
        db.drop_collection(collection)
        deletions.append(collection)
    return Response({'Deleted collections':deletions})