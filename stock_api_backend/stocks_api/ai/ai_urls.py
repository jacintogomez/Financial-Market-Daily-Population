from django.urls import path
from . import ai_views

urlpatterns=[
    path("",ai_views.ai_summary,name="ai_summary"),
]