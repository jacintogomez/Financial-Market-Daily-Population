from unittest import TestCase
from unittest.mock import patch, MagicMock, call
from django.test import TestCase
from celery.result import AsyncResult
from datetime import datetime, timezone
from pymongo.collection import Collection
from .webhook_handler import WebhookTask
from .tasks import (
    webhook_push,
    populate_market_stocks,
    async_market_population,
    fill_fundamentals_data,
    fill_ipo_data,
    fill_all_data,
)

class CeleryTaskTests(TestCase):

    def test_webhook_push_success(self):
        results=[{'code':200},{'code':200}]
        id='id'
        category='category'
        with patch('stocks_api.webhook_handler.WebhookTask.send_webhook') as mock:
            result=webhook_push(results,id,category)
            mock.assert_called_once_with(status='success',task_id=id,message='Updated category successfully',result='Results')
        self.assertTrue(result['success'])
        self.assertEqual(result['message'],'Updated category successfully')

    def test_webhook_push_failure(self):
        results=[{'code':200},{'code':400}]
        id='id'
        category='category'
        with patch('stocks_api.webhook_handler.WebhookTask.send_webhook') as mock:
            result=webhook_push(results,id,category)
            mock.assert_called_once_with(status='failure',task_id=id,message='Failed to update category',result='Results')
        self.assertFalse(result['success'])
        self.assertEqual(result['message'],'Failed to update category')

    @patch('stocks_api.tasks.fetch_fundamentals_data')
    @patch('stocks_api.tasks.fill_fundamentals_data.apply_async',side_effect=lambda *args,**kwargs:None)
    def test_fill_fundamentals_data_success(self,mockasync,mockfetch):
        mock=MagicMock()
        mock.status_code=200
        mock.data={
            'symbol':'DUOL',
        }
        mockfetch.return_value=mock
        results=fill_fundamentals_data()
        self.assertIn('finished updating fundamentals',results['message'])

    @patch('stocks_api.tasks.fetch_ipo_calendar_data')
    @patch('stocks_api.tasks.fill_ipo_data.apply_async',side_effect=lambda *args,**kwargs:None)
    def test_fill_ipo_data_success(self,mockasync,mockfetch):
        mock=MagicMock()
        mock.status_code=200
        mock.data={
            'ipo-calendar-confirmed':[],
            'ipo-calendar-prospectus':[],
            'ipo-calendar':[],
        }
        mockfetch.return_value=mock
        results=fill_ipo_data()
        self.assertIn('finished updating ipos',results['message'])

