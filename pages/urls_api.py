from django.urls import path
from . import views_api

urlpatterns = [
    # v1 포함
    path("v1/main/", views_api.main_api_view),
    path("v1/episode/pick/", views_api.pick_episode_api_view),
    path("v1/episode/random/", views_api.random_episode_api_view),
    path("v1/restore-db/", views_api.restore_db_api_view),
    # v1 미포함
    path("main/", views_api.main_api_view),
    path("episode/pick/", views_api.pick_episode_api_view),
    path("episode/random/", views_api.random_episode_api_view),
    path("restore-db/", views_api.restore_db_api_view),
]
