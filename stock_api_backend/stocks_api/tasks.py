from celery import shared_task
from .use_cases.get_stock_data import fetch_all_symbols_from_market,fetch_market_exchange_data
from .interfaces.mongodb_handler import save_asset_to_mongo,save_market_to_mongo
from .webhook_handler import WebhookTask

@shared_task(bind=True,max_retries=3)
def populate_market_stocks(self,market_ticker):
    try:
        code,symbols=fetch_all_symbols_from_market(market_ticker)
        for symbol in symbols[:5]:
            save_asset_to_mongo(symbol,market_ticker)
        return code
    except Exception as e:
        raise self.retry(exc=e,countdown=2**self.request.retries)

@shared_task(bind=True,base=WebhookTask)
def async_market_population(self):
    self.success_msg='Market data population completed successfully',
    self.failure_msg='Market data population failed',
    print('starting population task')
    code,markets=fetch_market_exchange_data()
    for market in markets[:5]:
        save_market_to_mongo(market)
        populate_market_stocks.delay(market['Code'])
    return code