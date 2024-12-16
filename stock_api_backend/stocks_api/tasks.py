from celery import shared_task
from .use_cases.get_stock_data import fetch_all_symbols_from_market, fetch_market_exchange_data
from .interfaces.mongodb_handler import save_to_mongo

@shared_task(bind=True, max_retries=3)
def populate_market_stocks(self, market_code):
    print('in shared task')
    try:
        # Fetch symbols for the market
        code, symbols = fetch_all_symbols_from_market(market_code)

        # Limit number of symbols to prevent overwhelming the system
        for symbol in symbols[:3]:  # Adjust limit as needed
            print('symbol is ',symbol)
            save_to_mongo(symbol, market_code)

    except Exception as exc:
        print('exception')
        # Retry the task with exponential backoff
        raise self.retry(exc=exc, countdown=2 ** self.request.retries)

@shared_task
def async_market_population():
    # Fetch market exchange data
    code, markets = fetch_market_exchange_data()
    print('in async func')
    # Queue population tasks for each market
    for market in markets[:3]:  # Limit to first 5 markets
        print('market is ',market)
        populate_market_stocks.delay(market['Code'])