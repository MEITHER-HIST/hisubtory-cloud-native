from django.urls import path
from . import views_api

urlpatterns = [
    path("v1/main/", views_api.main_api_view, name="main_api"),
    path("v1/restore-db/", views_api.restore_db_api_view, name="restore_db_api"),
]
