from django.urls import path
from . import views_api

urlpatterns = [
    # Pages API
    path("v1/main/", views_api.main_api_view),
    path("v1/episode/pick/", views_api.pick_episode_api_view),
    path("v1/episode/random/", views_api.random_episode_api_view),
    
    # User API
    path("v1/auth/mock-login/", views_api.mock_login_api_view),
    path("v1/auth/me/", views_api.me_api_view),
    
    # Story API (중요: 에피소드 상세 조회 404 해결용)
    path("episode/detail/", views_api.episode_detail_view),
]
