from celery import shared_task
from .kafka_producer import send_message
from .use_cases.get_stock_data import fetch_all_symbols_from_market,fetch_market_exchange_data
from .interfaces.mongodb_handler import save_asset_to_mongo,save_market_to_mongo

@shared_task(bind=True,max_retries=3)
def populate_market_stocks(self,market_ticker):
    try:
        code,symbols=fetch_all_symbols_from_market(market_ticker)
        for symbol in symbols[:3]:
            save_asset_to_mongo(symbol,market_ticker)
        return code
    except Exception as e:
        raise self.retry(exc=e,countdown=2**self.request.retries)

@shared_task
def async_market_population():
    print('starting population task')
    code,markets=fetch_market_exchange_data()
    for market in markets[:3]:
        save_market_to_mongo(market)
        populate_market_stocks.delay(market['Code'])
    send_message('market_data','population_complete','Database population bas been completed successfully')
    return code