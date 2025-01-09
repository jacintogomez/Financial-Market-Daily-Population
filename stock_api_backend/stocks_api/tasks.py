from celery import shared_task,group,chord,chain
from celery.result import GroupResult
from .use_cases.get_stock_data import fetch_all_symbols_from_market,fetch_market_exchange_data
from .interfaces.mongodb_handler import save_asset_to_mongo,save_market_to_mongo
from .webhook_handler import WebhookTask
from .domain.apiresponse.model.models import APIResponse
from .domain.fundamentals.model.models import Fundamentals
from .domain.fundamentals.service.fundamentals_service import fetch_fundamentals_data
from .domain.ipo.model.models import IPO
from .domain.ipo.service.ipo_service import fetch_ipo_calendar_data
from django.http import JsonResponse
from decouple import config
from pymongo import MongoClient
import logging
from datetime import datetime,timezone

mongo_uri=config('MONGO_URI')
client=MongoClient(mongo_uri)
db=client[config('MONGODB_DB_NAME')]
assets_collection=db['market_symbols']

logger=logging.getLogger('django')

@shared_task
def webhook_push(results,task_id,category=None,given_message=None):
    success=all(result.get('code')==200 for result in results)
    if not given_message:
        message=f'Updated {category} successfully' if success else f'Failed to update {category}'
    else:
        message=given_message
    WebhookTask.send_webhook(
        status='success' if success else 'failure',
        task_id=task_id,
        message=message,
        result='Results',
    )
    return {
        'success': success,
        'message': message,
    }

@shared_task(bind=True,max_retries=3)
def populate_market_stocks(self,market_ticker):
    try:
        code,symbols=fetch_all_symbols_from_market(market_ticker)
        symbol_errors=[]
        if symbols is None or not symbols:
            msg=f'Data not found for asset with symbol {market_ticker}'
            logger.error(msg)
            raise Exception(msg)
        for symbol in symbols[:5]:
            try:
                save_asset_to_mongo(symbol,market_ticker)
            except Exception as e:
                msg=f'Failed to save asset with symbol {symbol}: {e}'
                logger.error(msg)
                symbol_errors.append(msg)
        if symbol_errors:
            msg=f"Asset save errors for market {market_ticker}: {'; '.join(symbol_errors)}"
            logger.error(msg)
            raise Exception(msg)
        msg=f'All assets saved successfully for market {market_ticker}'
        logger.info(msg)
        return {
            'code': code,
            'message': msg,
        }
    except Exception as e:
        raise self.retry(exc=e,countdown=2**self.request.retries)

@shared_task(bind=True,base=WebhookTask)
def async_market_population(self):
    logger.info(f'Started updating all market symbols at {datetime.now(timezone.utc).isoformat()}')
    try:
        code,markets=fetch_market_exchange_data()
        market_errors=[]
        for market in markets[:5]:
            try:
                save_market_to_mongo(market)
            except Exception as e:
                msg=f'Failed to save market symbols for {market}: {str(e)}'
                logger.error(msg)
                market_errors.append(msg)
        if market_errors:
            msg=f'Error saving market symbol data: {market_errors}'
            logger.error(msg)
            raise Exception(msg)
        market_symbols_update_tasks=[populate_market_stocks.s(market['Code']) for market in markets[:5]]
        market_symbols_callback=webhook_push.s(task_id=self.request.id,category='market symbols')
        data_filling=fill_all_data.s()
        flow=(chord(market_symbols_update_tasks,market_symbols_callback)|data_filling)
        flow.delay()
        return {
            'code': code,
            'message': f'Database symbol update started.',
        }
    except Exception as e:
        msg=f'Error updating market symbols: {str(e)}'
        logger.error(msg)
        raise Exception(msg)

@shared_task
def process_fundamentals(symbol):
    fundamentals_response=fetch_fundamentals_data(symbol)
    fundamentals=Fundamentals(symbol=symbol,provider='EOD')
    if fundamentals_response.status_code==200:
        fundamentals.upsert_asset(symbol,fundamentals_response.data)
        return {'symbol':symbol,'status':'success'}
    else:
        msg=f'Failed to fetch fundamentals for {symbol}: Status code {fundamentals_response.status_code}'
        logger.error(msg)
        return {'symbol':symbol,'status':'failure','error':msg}

@shared_task(bind=True,base=WebhookTask)
def fill_fundamentals_data(self):
    fundamentals_errors=[]
    try:
        cursor=assets_collection.find(batch_size=100)
        symbols=[symbol['Code'] for symbol in cursor]
        fund_task_group=group(process_fundamentals.s(symbol) for symbol in symbols)
        results=fund_task_group.apply_async()
        failed_tasks=[result for result in results.get() if result['status']=='failed']
        if failed_tasks:
            errors='; '.join([f"{task['symbol']}: {task.get('error','Unknown error')}" for task in failed_tasks])
            logger.error(errors)

        return {'message':'finished updating fundamentals','partial-errors':f"{'; '.join(fundamentals_errors)}"}

    except Exception as e:
        msg=f'Error while filling fundamentals data: {str(e)}'
        logger.error(msg)
        raise Exception(msg)

@shared_task(bind=True,base=WebhookTask)
def fill_ipo_data(self):
    ipo_errors=[]
    try:
        ipo_response=fetch_ipo_calendar_data()
        ipo=IPO(symbol='IPO Calendar',provider='FMP')
        if ipo_response.status_code in [200,206]:
            ipo.upsert_asset('IPO Calendar',ipo_response.data['ipo-calendar-confirmed'],ipo_response.data['ipo-calendar-prospectus'],ipo_response.data['ipo-calendar'])
            return {'message':'finished updating ipos'}
        else:
            msg=f'Failed to fetch IPO calendar data: Status code {ipo_response.status_code}'
            logger.error(msg)
            ipo_errors.append(msg)

        return {'message':'finished updating fundamentals','partial-errors':f"{'; '.join(ipo_errors)}"}

    except Exception as e:
        msg=f'Error while filling IPO data: {str(e)}'
        logger.error(msg)
        raise Exception(msg)

@shared_task(bind=True,base=WebhookTask)
def fill_all_data(self,previous_result=None):
    logger.info(f'Started updating market data at {datetime.now(timezone.utc).isoformat()}')
    try:
        fill_all_data_tasks=[
            fill_fundamentals_data.s(),
            fill_ipo_data.s(),
        ]
        data_filled_callback=webhook_push.s(task_id=self.request.id,given_message='Finished daily re-run')
        chord(fill_all_data_tasks,data_filled_callback).delay()

        return {'message':'Daily re-run started'}

    except Exception as e:
        msg=f'Error during daily data update: {str(e)}'
        logger.error(msg)
        raise Exception(msg)
