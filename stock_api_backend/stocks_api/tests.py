from unittest.mock import patch, MagicMock, call
from django.test import TestCase
from celery.result import AsyncResult
from .domain.ipo.model.models import IPO
from .tasks import (
    webhook_push,
    populate_market_stocks,
    async_market_population,
    fill_fundamentals_data,
    fill_ipo_data,
    fill_all_data
)

class WebhookTaskTests(TestCase):
    def setUp(self):
        self.task_id = "test-task-123"

    @patch('tasks.WebhookTask.send_webhook')
    def test_webhook_push_success(self, mock_send_webhook):
        results = [{'code': 200}, {'code': 200}]
        result = webhook_push(results, self.task_id, category='test')

        mock_send_webhook.assert_called_once_with(
            status='success',
            task_id=self.task_id,
            message='Updated test successfully',
            result='Results'
        )
        self.assertTrue(result['success'])

    @patch('tasks.WebhookTask.send_webhook')
    def test_webhook_push_failure(self, mock_send_webhook):
        results = [{'code': 200}, {'code': 400}]
        result = webhook_push(results, self.task_id, category='test')

        mock_send_webhook.assert_called_once_with(
            status='failure',
            task_id=self.task_id,
            message='Failed to update test',
            result='Results'
        )
        self.assertFalse(result['success'])

class PopulateMarketStocksTests(TestCase):
    @patch('tasks.fetch_all_symbols_from_market')
    @patch('tasks.save_asset_to_mongo')
    def test_populate_market_stocks_success(self, mock_save, mock_fetch):
        mock_fetch.return_value = (200, [{'symbol': 'AAPL'}, {'symbol': 'GOOGL'}])

        result = populate_market_stocks.apply(args=('NYSE',)).get()

        self.assertEqual(result['code'], 200)
        self.assertTrue('successfully' in result['message'])
        mock_save.assert_has_calls([
            call({'symbol': 'AAPL'}, 'NYSE'),
            call({'symbol': 'GOOGL'}, 'NYSE')
        ])

class IPODataTests(TestCase):
    @patch('ipo_service.requests.get')
    def test_fetch_ipo_calendar_data_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'confirmed': ['IPO1', 'IPO2'],
            'prospectus': ['IPO3'],
            'calendar': ['IPO4', 'IPO5']
        }
        mock_get.return_value = mock_response

        with patch('tasks.IPO') as mock_ipo:
            mock_instance = MagicMock()
            mock_ipo.return_value = mock_instance

            result = fill_ipo_data.apply().get()

            self.assertEqual(result['message'], 'finished updating ipos')
            mock_instance.upsert_asset.assert_called_once()

    def test_ipo_model_to_dict(self):
        ipo = IPO(
            symbol='TEST',
            ipo_confirmed={'test': 'data'},
            ipo_prospectus={'more': 'data'},
            provider='FMP'
        )
        result = ipo.to_dict()

        self.assertEqual(result['symbol'], 'TEST')
        self.assertEqual(result['provider'], 'FMP')
        self.assertIn('ipo_confirmed', result)
        self.assertIn('ipo_prospectus', result)

class AsyncMarketPopulationTests(TestCase):
    @patch('tasks.fetch_market_exchange_data')
    @patch('tasks.save_market_to_mongo')
    @patch('tasks.chord')
    def test_async_market_population_success(self, mock_chord, mock_save, mock_fetch):
        mock_fetch.return_value = (200, [{'Code': 'NYSE'}, {'Code': 'NASDAQ'}])
        mock_chord.return_value.delay.return_value = AsyncResult('test-id')

        result = async_market_population.apply().get()

        self.assertEqual(result['code'], 200)
        self.assertTrue('started' in result['message'])
        mock_save.assert_has_calls([
            call({'Code': 'NYSE'}),
            call({'Code': 'NASDAQ'})
        ])
        mock_chord.assert_called_once()