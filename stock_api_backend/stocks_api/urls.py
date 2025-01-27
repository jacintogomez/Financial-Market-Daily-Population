from django.urls import path
from . import views

urlpatterns = [
    path('stocks/<str:symbol>',views.get_stock_data),
    path('pushtodb/<str:symbol>/<str:provider>/<str:collection>',views.push_to_db_test),
    path('market_exchange/',views.get_market_exchange_data),
    path('update_fundamentals/',views.update_fundamentals),
    path('update_ipo/',views.update_ipo),
    path('update_esg/',views.update_esg),
    path('update_news/',views.update_news),
    path('update_fundraising/',views.update_fundraising),
    path('update_mergers_acquisitions/',views.update_mergers_acquisitions),
    path('update_rating/',views.update_rating),
    path('update_earnings/',views.update_earnings),
    path('get_fmp_symbols_data/',views.get_fmp_symbols_data),
    path('clear_collections/',views.clear_test_collections), #TODO delete this endpoint
    path('display/',views.display_all_symbols),
    path('webhook/',views.webhook_receiver,name='webhook_receiver'),
    path('get_info/<str:collection_name>/<path:field_path>/<str:query_value>/',views.get_info),
    path('get_info/<str:collection_name>/<path:field_path>/',views.get_info),
]