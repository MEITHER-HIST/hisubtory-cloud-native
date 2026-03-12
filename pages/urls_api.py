from django.urls import path
from . import views_api

urlpatterns = [
    # 1. Pages 관련 API (V1 포함)
    path("v1/main/", views_api.main_api_view),
    path("v1/episode/pick/", views_api.pick_episode_api_view),
    path("v1/episode/random/", views_api.random_episode_api_view),
    path("v1/restore-db/", views_api.restore_db_api_view), # 💡 누락된 경로 추가
    
    # 💡 v1 없이 들어오는 요청도 처리
    path("main/", views_api.main_api_view),
    path("episode/pick/", views_api.pick_episode_api_view),
    path("episode/random/", views_api.random_episode_api_view),
    path("restore-db/", views_api.restore_db_api_view),

    # 2. Accounts 관련 API (V1 포함)
    path("v1/login/", views_api.mock_login_api_view),
    path("v1/logout/", views_api.logout_api_view),
    path("v1/me/", views_api.me_api_view),
    path("v1/signup/", views_api.mock_login_api_view),
    path("v1/csrf/", views_api.me_api_view),

    # 💡 v1 없이 들어오는 요청도 처리
    path("login/", views_api.mock_login_api_view),
    path("logout/", views_api.logout_api_view),
    path("me/", views_api.me_api_view),
    path("signup/", views_api.mock_login_api_view),
    path("csrf/", views_api.me_api_view),
    
    # 3. Stories 관련 API
    path("v1/episode/detail/", views_api.episode_detail_view),
    path("episode/detail/", views_api.episode_detail_view),
    
    # 4. 기타 경로
    path("v1/auth/mock-login/", views_api.mock_login_api_view),
    path("v1/auth/me/", views_api.me_api_view),
]
