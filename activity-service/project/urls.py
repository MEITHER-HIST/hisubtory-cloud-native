from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse

urlpatterns = [
    path('health/', lambda r: HttpResponse('ok')),
    path('admin/', admin.site.urls),
    # 💡 여기서 중복된 api/pages/ 를 제거하고 pages.urls_api로 넘깁니다.
    path("api/pages/", include("pages.urls_api")),
    path("", include("pages.urls_api")),
]
