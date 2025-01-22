from ..domain.models import Asset

def post_stock_data_to_collection(symbol,provider,collection,data):
    stock=Asset(symbol=symbol,provider=provider,collection=collection)
    stock_data={'data':data}
    stock.upsert_asset(symbol,stock_data['data'],collection)
    return 200