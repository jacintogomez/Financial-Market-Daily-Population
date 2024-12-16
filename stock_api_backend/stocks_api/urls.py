from django.urls import path
from .views import get_all_stocks_from_market, get_stock_data, get_multi_stock_data, get_fundamentals, get_market_exchange_data, get_assets_under_market

urlpatterns = [
    path('stocks/<str:market_ticker>',get_all_stocks_from_market),
    path('stocks/<str:symbol>',get_stock_data),
    path('stocks/<str:stocks>',get_multi_stock_data),
    path('fundamentals/',get_fundamentals),
    #path('market_exchange_data/<str:market_ticker>',get_assets_under_market),
    path('market_exchange/',get_market_exchange_data),
]