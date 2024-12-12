from django.urls import path
from .views import get_all_stocks,get_stock_data,get_multi_stock_data,get_fundamentals

urlpatterns = [
    path('stocks/',get_all_stocks),
    path('stocks/<str:symbol>',get_stock_data),
    path('stocks/<str:stocks>',get_multi_stock_data),
    path('fundamentals/',get_fundamentals),
]