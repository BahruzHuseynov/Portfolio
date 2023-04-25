from django.urls import path
from core import views

app_name = 'core'

urlpatterns = [
    path("", views.BaseIndexView.as_view(), name="index"),
    path("check-urls-status/", views.check_urls_status, name="check_urls_status"),
]
