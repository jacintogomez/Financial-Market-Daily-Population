from datetime import datetime, timezone
from typing import Generic, Optional, TypeVar
from rest_framework.renderers import JSONRenderer
from django.http import HttpResponse
import json
from decimal import Decimal

class APIResponseRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        if hasattr(data, 'to_dict'):
            response_data = data.to_dict()
            return super().render(response_data, accepted_media_type, renderer_context)
        return super().render(data, accepted_media_type, renderer_context)

class FundamentalsData:
    def __init__(self):
        self.parameters=0
    def convert_data_to_dict(self):
        return self.__dict__

class APIResponse:
    def __init__(self,code,message,data=None):
        self.timestamp=datetime.now(timezone.utc).isoformat()
        self.status_code=code
        self.message=message
        self.data=data
    def to_dict(self):
        return {
            'timestamp': self.timestamp,
            'status_code': self.status_code,
            'data': self.data if self.data else None,
            'message': self.message,
        }

class ErrorDetails:
    def __init__(self,status,details,field):
        self.status_code=status
        self.details=details
        self.field=field

