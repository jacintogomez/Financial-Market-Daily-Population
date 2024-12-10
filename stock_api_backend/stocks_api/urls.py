from django.urls import path
from .views import get_all_stocks,get_stock_data

urlpatterns = [
    path('stocks/',get_all_stocks),
    path('stocks/<str:symbol>',get_stock_data), #provider is the API provider, FMP for example
]