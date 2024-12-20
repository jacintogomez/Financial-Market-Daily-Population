from django.urls import path
from .views import get_stock_data, get_multi_stock_data, get_market_exchange_data,clear_test_collections, push_to_db_test

urlpatterns = [
    path('stocks/<str:symbol>',get_stock_data),
    path('pushtodb/<str:symbol>/<str:provider>/<str:collection>',push_to_db_test),
    #path('market_exchange_data/<str:market_ticker>',get_assets_under_market),
    path('market_exchange/',get_market_exchange_data),
    path('clear_collections/',clear_test_collections), # needs to be deleted at some point
]