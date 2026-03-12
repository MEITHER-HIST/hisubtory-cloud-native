from django.urls import path
from . import views_api

urlpatterns = [
    # v1 접두사가 붙은 경로
    path("v1/main/", views_api.main_api_view),
    path("v1/episode/pick/", views_api.pick_episode_api_view),
    path("v1/episode/random/", views_api.random_episode_api_view),
    path("v1/restore-db/", views_api.restore_db_api_view),
    
    # 접두사 없는 경로 (Nginx에서 이미 떼고 보내는 경우 대비)
    path("main/", views_api.main_api_view),
    path("episode/pick/", views_api.pick_episode_api_view),
    path("episode/random/", views_api.random_episode_api_view),
    path("restore-db/", views_api.restore_db_api_view),
]
