from unittest import TestCase
from unittest.mock import patch, MagicMock, call
from django.test import TestCase
from celery.result import AsyncResult
from datetime import datetime, timezone
from pymongo.collection import Collection
from .tasks import (
    webhook_push,
    populate_market_stocks,
    async_market_population,
    fill_fundamentals_data,
    fill_ipo_data,
    fill_all_data,
)

class CeleryTasksTests(TestCase):
    def setUp(self):
        self.mock_assets_collection = patch('tasks.assets_collection').start()
        self.addCleanup(patch.stopall)

    def test_webhook_push_success(self):
        results = [{'code': 200}, {'code': 200}]
        task_id = 'test-task-id'
        category = 'test-category'

        with patch('tasks.WebhookTask.send_webhook') as mock_webhook:
            result = webhook_push(results, task_id, category)

            mock_webhook.assert_called_once_with(
                status='success',
                task_id=task_id,
                message='Updated test-category successfully',
                result='Results'
            )
            self.assertTrue(result['success'])
            self.assertEqual(result['message'], 'Updated test-category successfully')

    def test_webhook_push_failure(self):
        results = [{'code': 200}, {'code': 400}]
        task_id = 'test-task-id'
        category = 'test-category'

        with patch('tasks.WebhookTask.send_webhook') as mock_webhook:
            result = webhook_push(results, task_id, category)

            mock_webhook.assert_called_once_with(
                status='failure',
                task_id=task_id,
                message='Failed to update test-category',
                result='Results'
            )
            self.assertFalse(result['success'])

    @patch('tasks.fetch_all_symbols_from_market')
    @patch('tasks.save_asset_to_mongo')
    def test_populate_market_stocks_success(self, mock_save_asset, mock_fetch_symbols):
        mock_fetch_symbols.return_value = (200, ['AAPL', 'GOOGL', 'MSFT'])

        result = populate_market_stocks('NYSE')

        mock_fetch_symbols.assert_called_once_with('NYSE')
        self.assertEqual(mock_save_asset.call_count, 3)
        self.assertEqual(result['code'], 200)
        self.assertIn('All assets saved successfully', result['message'])

    @patch('tasks.fetch_market_exchange_data')
    @patch('tasks.save_market_to_mongo')
    @patch('tasks.chord')
    def test_async_market_population_success(self, mock_chord, mock_save_market, mock_fetch_markets):
        markets = [{'Code': 'NYSE'}, {'Code': 'NASDAQ'}]
        mock_fetch_markets.return_value = (200, markets)

        result = async_market_population()

        mock_fetch_markets.assert_called_once()
        self.assertEqual(mock_save_market.call_count, 2)
        mock_chord.assert_called()
        self.assertEqual(result['code'], 200)
        self.assertIn('Database symbol update started', result['message'])

    @patch('tasks.fetch_fundamentals_data')
    def test_fill_fundamentals_data(self, mock_fetch_fundamentals):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.data = {'someKey': 'someValue'}
        mock_fetch_fundamentals.return_value = mock_response

        self.mock_assets_collection.find.return_value = [{'Code': 'AAPL'}, {'Code': 'GOOGL'}]

        result = fill_fundamentals_data()

        self.assertEqual(mock_fetch_fundamentals.call_count, 2)
        self.assertIn('finished updating fundamentals', result['message'])

    @patch('tasks.fetch_ipo_calendar_data')
    def test_fill_ipo_data_success(self, mock_fetch_ipo):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.data = {
            'ipo-calendar-confirmed': [],
            'ipo-calendar-prospectus': [],
            'ipo-calendar': []
        }
        mock_fetch_ipo.return_value = mock_response

        result = fill_ipo_data()

        mock_fetch_ipo.assert_called_once()
        self.assertIn('finished updating ipos', result['message'])

    @patch('tasks.chord')
    def test_fill_all_data(self, mock_chord):
        result = fill_all_data()

        mock_chord.assert_called_once()
        self.assertIn('Daily re-run started', result['message'])

    def test_populate_market_stocks_retry_on_failure(self):
        with patch('tasks.fetch_all_symbols_from_market') as mock_fetch:
            mock_fetch.side_effect = Exception('API Error')

            with self.assertRaises(Exception):
                populate_market_stocks('NYSE')

            self.assertEqual(mock_fetch.call_count, 1)

    @patch('tasks.logger')
    def test_fill_fundamentals_data_handles_errors(self, mock_logger):
        self.mock_assets_collection.find.return_value = [{'Code': 'AAPL'}]

        with patch('tasks.fetch_fundamentals_data') as mock_fetch:
            mock_fetch.side_effect = Exception('API Error')

            result = fill_fundamentals_data()

            mock_logger.error.assert_called()
            self.assertIn('partial-errors', result)