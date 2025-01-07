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
