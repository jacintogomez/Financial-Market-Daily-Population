from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime,timezone
import platform

@api_view(['GET'])
def health_check(request):
    """Endpoint returning health status of system"""
    return Response({
        'status':'healthy',
        'timestamp':datetime.now(timezone.utc).isoformat(),
        'system_info':{
            'python_version':platform.python_version(),
        },
        'message':'OK'
    },status=status.HTTP_200_OK)