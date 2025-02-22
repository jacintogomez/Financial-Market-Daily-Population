from django.http import JsonResponse
from pymongo import MongoClient
from decouple import config
from rest_framework.response import Response
from ..utils import APIResponse

mongo_uri=config('MONGO_URI')
client=MongoClient(mongo_uri)

db=client[config('MONGODB_DB_NAME')]
exchanges_collection=db['market_exchanges']
assets_collection=db['market_symbols'] #equivalent of market_eod_symbols
fmp_assets_collection=db['market_fmp_symbols']

def save_asset_to_mongo(asset,provider):
    if provider=='EOD':
        market=asset['Exchange']
        query={'Code':asset['Code'],'Exchange':market}
        print('updating asset')
        # $set:data will
        # upsert=True will update a record with matching ticker, and if there is no match it will create a new record
        assets_collection.update_one(query,{'$set':asset},upsert=True)
        response=APIResponse(200,f'Saved asset with code {asset["Code"]} to assets collection',None)
        return JsonResponse(response.to_dict())
    else:
        market=asset['exchangeShortName']
        query={'symbol':asset['symbol'],'exchangeShortName':market}
        print('updating asset')
        fmp_assets_collection.update_one(query,{'$set':asset},upsert=True)
        response=APIResponse(200,f'Saved asset with code {asset["symbol"]} to assets collection',None)
        return JsonResponse(response.to_dict())

def save_market_to_mongo(market):
    print('updating market')
    query={'Code':market['Code']}
    exchanges_collection.update_one(query,{'$set':market},upsert=True)
    response=APIResponse(200,f'Saved market with code {market["Code"]} to exchanges collection',None)
    return JsonResponse(response.to_dict())

def is_asset_in_mongo(symbol):
    query={'Symbol':symbol}
    asset=assets_collection.find_one(query)
    print('asset',asset)
    return asset is not None #TODO do we need an APIResponse for this?
    # if asset:
    #     response=APIResponse(200,f'Asset with symbol {symbol} found',True)
    # else:
    #     response=APIResponse(200,f'Asset with symbol {symbol} not found',False)
    # return JsonResponse(response.to_dict())

def fetch_from_mongo_collection(market):
    # {} is used to find all documents; no filters
    # {'_id':0} ignores the MongoDB mandatory _id field
    return list(db[market].find({},{'_id':0}))

def display_all_symbols_from_mongo():
    cursor=assets_collection.find(batch_size=100)
    for symbol in cursor:
        print(symbol)

def drop_collections_from_mongo():
    # This is just for testing purposes obviously, will not be in the real thing
    deletions=[]
    print('dropping all')
    collections=[exchanges_collection,assets_collection]
    for collection in collections:
        db.drop_collection(collection)
        deletions.append(collection)
    return Response({'Deleted collections':deletions})