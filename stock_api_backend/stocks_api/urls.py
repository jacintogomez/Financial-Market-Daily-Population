from django.urls import path
from . import views
from .views import get_stock_data, get_market_exchange_data,clear_test_collections, push_to_db_test,update_all_collections,display_all_symbols

urlpatterns = [
    path('stocks/<str:symbol>',get_stock_data),
    path('pushtodb/<str:symbol>/<str:provider>/<str:collection>',push_to_db_test),
    path('market_exchange/',get_market_exchange_data),
    path('update_all_collections/',update_all_collections),
    path('clear_collections/',clear_test_collections), #TODO delete this endpoint
    path('display/',display_all_symbols),
    path('webhook/',views.webhook_receiver,name='webhook_receiver'),
]