from django.urls import path
from .views import get_all_stocks,get_stock_data

urlpatterns = [
    path('stocks/',get_all_stocks),
    path('stocks/<str:symbol>/<str:provider>',get_stock_data),
]