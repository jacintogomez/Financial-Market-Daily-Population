from celery import shared_task,group,chord
from celery.result import GroupResult
from .use_cases.get_stock_data import fetch_all_symbols_from_market,fetch_market_exchange_data
from .interfaces.mongodb_handler import save_asset_to_mongo,save_market_to_mongo
from .webhook_handler import WebhookTask
from .domain.apiresponse.model.models import APIResponse
from django.http import JsonResponse

@shared_task
def webhook_push(results,task_id):
    success=all(result.get('code')==200 for result in results)
    message='All markets populated successfully' if success else 'Failure in market population'
    webhook=WebhookTask()
    if success:
        webhook.on_success({'message':message},task_id,[],{})
    else:
        webhook.on_failure(Exception(message),task_id,[],{},None)
    print('time to send a message')
    # return {
    #     'success': success,
    #     'message': message,
    # }

@shared_task(bind=True,max_retries=3)
def populate_market_stocks(self,market_ticker):
    try:
        code,symbols=fetch_all_symbols_from_market(market_ticker)
        symbol_errors=[]
        if symbols is None or not symbols:
            raise Exception(f'Data not found for asset with symbol {market_ticker}')
        for symbol in symbols[:5]:
            print('populating stock',symbol)
            try:
                save_asset_to_mongo(symbol,market_ticker)
            except Exception as e:
                symbol_errors.append(f'Failed to save asset with symbol {symbol}: {e}')
        if symbol_errors:
            raise Exception(f"Asset save errors for market {market_ticker}: {'; '.join(symbol_errors)}")
        return {
            'code': code,
            'message': f'All assets saved successfully for market {market_ticker}',
        }
    except Exception as e:
        raise self.retry(exc=e,countdown=2**self.request.retries)

@shared_task(bind=True,base=WebhookTask)
def async_market_population(self):
    print('starting population task')
    try:
        code,markets=fetch_market_exchange_data()
        market_errors=[]
        for market in markets[:5]:
            try:
                save_market_to_mongo(market)
            except Exception as e:
                market_errors.append(f'Failed to save market {market}: {str(e)}')
        if market_errors:
            raise Exception(f'Error saving market data: {market_errors}')
        # market_population_tasks=group(populate_market_stocks.s(market['Code']) for market in markets[:5])
        # result=group(market_population_tasks).apply_async()
        # result.get()
        market_population_tasks=[populate_market_stocks.s(market['Code']+'str') for market in markets[:5]]
        callback=webhook_push.s(task_id=self.request.id)
        chord(market_population_tasks)(callback)
        return {
            'code': code,
            'message': f'Database population started.',
        }
    except Exception as e:
        raise Exception(f'Error populating database with market data: {str(e)}')