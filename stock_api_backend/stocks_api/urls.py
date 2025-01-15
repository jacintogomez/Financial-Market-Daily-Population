from django.urls import path
from .views import (
    get_stock_data,
    get_market_exchange_data,
    clear_test_collections,
    push_to_db_test,
    update_fundamentals,
    update_ipo,
    update_mergers_acquisitions,
    update_fundraising,
    update_news,
    display_all_symbols,
    webhook_receiver,
)

urlpatterns = [
    path('stocks/<str:symbol>',get_stock_data),
    path('pushtodb/<str:symbol>/<str:provider>/<str:collection>',push_to_db_test),
    path('market_exchange/',get_market_exchange_data),
    path('update_fundamentals/',update_fundamentals),
    path('update_ipo/',update_ipo),
    path('update_news/',update_news),
    path('update_fundraising/',update_fundraising),
    path('update_mergers_acquisitions/',update_mergers_acquisitions),
    path('clear_collections/',clear_test_collections), #TODO delete this endpoint
    path('display/',display_all_symbols),
    path('webhook/',webhook_receiver,name='webhook_receiver'),
]