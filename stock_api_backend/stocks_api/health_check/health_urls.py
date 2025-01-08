from django.urls import path
from .health_views import health_check,health_unit_tests

urlpatterns=[
    path('',health_check,name='health_check'),
    path('tests/',health_unit_tests,name='health_unit_tests'),
]