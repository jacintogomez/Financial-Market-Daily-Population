import traceback

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime,timezone
import platform
from django.test.runner import DiscoverRunner
from contextlib import redirect_stdout
import io

@api_view(['GET'])
def health_check(request):
    """Endpoint returning health status of system"""
    return Response({
        'status':'healthy',
        'timestamp':datetime.now(timezone.utc).isoformat(),
        'system_info':{
            'python_version':platform.python_version(),
        },
        'message':'OK',
    },status=status.HTTP_200_OK)

from django.test.utils import get_runner
from django.conf import settings

@api_view(['GET'])
def health_unit_tests(request):
    try:
        import unittest
        import sys

        # Capture stdout
        output = io.StringIO()
        runner = unittest.TextTestRunner(stream=output, verbosity=0)

        # Get all tests from the stocks_api app
        from django.apps import apps
        app_config = apps.get_app_config('stocks_api')
        test_loader = unittest.TestLoader()
        tests = test_loader.discover(app_config.path, pattern='test*.py')

        with redirect_stdout(output):
            result = runner.run(tests)

        was_successful = result.wasSuccessful()

        return Response({
            'status': 'healthy' if was_successful else 'not healthy',
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'system_info': {
                'python_version': platform.python_version(),
            },
            'message': 'OK',
            'test_results': {
                'ran': result.testsRun,
                'errors': len(result.errors),
                'failures': len(result.failures),
            },
            'output': output.getvalue(),
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({
            'status': 'error',
            'error': str(e),
            'traceback': traceback.format_exc()  # Add this to get more detail
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)