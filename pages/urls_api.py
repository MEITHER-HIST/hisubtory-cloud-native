from django.urls import path
from . import views_api

urlpatterns = [
    # 1. Pages 관련 API
    path("v1/main/", views_api.main_api_view),
    path("v1/episode/pick/", views_api.pick_episode_api_view),
    path("v1/episode/random/", views_api.random_episode_api_view),
    
    # 2. Accounts 관련 API (프론트엔드 호출 주소 매칭)
    path("login/", views_api.mock_login_api_view),
    path("logout/", views_api.logout_api_view),
    path("me/", views_api.me_api_view),
    path("signup/", views_api.mock_login_api_view), # 가입도 로그인으로 대체
    path("csrf/", views_api.me_api_view), # CSRF 요청 대응
    
    # 3. Stories 관련 API
    path("episode/detail/", views_api.episode_detail_view),
    
    # 4. 기존 v1 경로 대응 (혹시 모를 상황 대비)
    path("v1/auth/mock-login/", views_api.mock_login_api_view),
    path("v1/auth/me/", views_api.me_api_view),
]
