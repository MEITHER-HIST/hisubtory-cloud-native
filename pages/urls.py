from django.urls import path
from . import views_api

urlpatterns = [
    path("v1/main/", views_api.main_api_view, name="main_api"),
    path("v1/episode/pick/", views_api.pick_episode_api_view, name="pick_episode_api"),
    path("v1/episode/random/", views_api.random_episode_api_view, name="random_episode_api"),
    
    # 💡 index-DObKs1_r.js 에서 요청하는 경로들이 activity-service(pages)로 올 경우 대비
    path("v1/me/", views_api.me_api_view, name="me_api"),
    path("v1/logout/", views_api.logout_api_view, name="logout_api"),
    path("v1/restore-db/", views_api.restore_db_api_view, name="restore_db_api"),
]
