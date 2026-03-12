from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse

urlpatterns = [
    path('health/', lambda r: HttpResponse('ok')),
    path('admin/', admin.site.urls),
    # /api/pages/ 로 들어오는 모든 것을 pages.urls_api로 보냄
    path("api/pages/", include("pages.urls_api")),
    # 혹시 Nginx가 /api/pages/ 를 떼고 보내면 여기서 처리
    path("", include("pages.urls_api")),
]
