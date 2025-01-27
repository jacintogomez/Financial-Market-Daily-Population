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
    update_esg,
    update_rating,
    update_earnings,
    get_fmp_symbols_data,
    update_news,
    display_all_symbols,
    webhook_receiver,
    get_info,
)

urlpatterns = [
    path('stocks/<str:symbol>',get_stock_data),
    path('pushtodb/<str:symbol>/<str:provider>/<str:collection>',push_to_db_test),
    path('market_exchange/',get_market_exchange_data),
    path('update_fundamentals/',update_fundamentals),
    path('update_ipo/',update_ipo),
    path('update_esg/',update_esg),
    path('update_news/',update_news),
    path('update_fundraising/',update_fundraising),
    path('update_mergers_acquisitions/',update_mergers_acquisitions),
    path('update_rating/',update_rating),
    path('update_earnings/',update_earnings),
    path('get_fmp_symbols_data/',get_fmp_symbols_data),
    path('clear_collections/',clear_test_collections), #TODO delete this endpoint
    path('display/',display_all_symbols),
    path('webhook/',webhook_receiver,name='webhook_receiver'),
    path('get_info/<str:collection_name>/<path:field_path>/<str:query_value>/',get_info),
    path('get_info/<str:collection_name>/<path:field_path>/',get_info),
]