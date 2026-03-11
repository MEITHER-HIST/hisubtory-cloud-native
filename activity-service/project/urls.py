from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse

def health(request):
    return HttpResponse("ok")

urlpatterns = [
    path('health/', health),
    path('admin/', admin.site.urls), # 관리자 페이지 추가
    path("api/pages/", include("pages.urls_api")),
    path("api/accounts/", include("pages.urls_api")),
    path("api/stories/", include("pages.urls_api")),
]
