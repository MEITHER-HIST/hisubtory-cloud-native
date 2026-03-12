from django.urls import path, include
from . import views_api

# 💡 공통 패턴 정의
inner_patterns = [
    path("main/", views_api.main_api_view),
    path("episode/pick/", views_api.pick_episode_api_view),
    path("episode/random/", views_api.random_episode_api_view),
    path("restore-db/", views_api.restore_db_api_view),
    path("login/", views_api.mock_login_api_view),
    path("logout/", views_api.logout_api_view),
    path("me/", views_api.me_api_view),
    path("signup/", views_api.mock_login_api_view),
    path("csrf/", views_api.me_api_view),
    path("episode/detail/", views_api.episode_detail_view),
]

urlpatterns = [
    # 1. /api/pages/v1/...
    path("api/pages/v1/", include(inner_patterns)),
    # 2. /api/pages/...
    path("api/pages/", include(inner_patterns)),
    # 3. /v1/...
    path("v1/", include(inner_patterns)),
    # 4. /...
    path("", include(inner_patterns)),
]
